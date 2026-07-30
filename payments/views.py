import requests
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from accounts.models import Student

from .models import (
    Package,
    PackageRequest,
    Payment,
    PaymentStatus,
    ServiceToStudent,
    DiscountUsage,
    PaymentProvider
)

def start_payment(request, package_id, provider):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "ابتدا وارد حساب کاربری شوید."},
            status=403
        )

    if request.user.role != "student":
        return JsonResponse(
            {"error": "فقط حساب داوطلب امکان خرید دارد."},
            status=403
        )

    package = get_object_or_404(
        Package,
        id=package_id
    )

    try:
        student = request.user.user_student
    except Student.DoesNotExist:
        return JsonResponse(
            {"error": "اطلاعات داوطلب یافت نشد."},
            status=400,
        )

    order = get_object_or_404(
        PackageRequest,
        student=student,
        package=package,
        paid=False
    )

    # دوباره اعتبار کد تخفیف بررسی شود
    if order.discount_code:

        valid, error = order.discount_code.is_valid(
            request.user,
            package,
            package.total_price
        )

        if not valid:

            order.discount_code = None
            order.discount_amount = 0
            order.final_price = package.total_price
            order.save()

            return JsonResponse(
                {
                    "error": error
                },
                status=400
            )

    if order.final_price <= 0:

        return JsonResponse(
            {
                "error": "این سفارش نیاز به پرداخت ندارد."
            },
            status=400
        )

    Payment.objects.filter(
        order=order,
        status=PaymentStatus.INIT
    ).delete()

    callback_url = request.build_absolute_uri(
        reverse("payment_verify")
    )

    if provider == "zarinpal":
        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(order.final_price) * 10,
            "description": f"پرداخت پکیج {package.id}",
            "callback_url": callback_url,
            "metadata": {
                "mobile": student.user.mobile
            }
        }
        
        response = requests.post(
            "https://payment.zarinpal.com/pg/v4/payment/request.json",
            json=data
        ).json()
        
        if response.get("data", {}).get("code") == 100:
        
            authority = response["data"]["authority"]
        
            Payment.objects.create(
                order=order,
                amount=order.final_price,
                authority=authority,
                provider=PaymentProvider.ZARINPAL,
            )
        
            return redirect(
                f"https://payment.zarinpal.com/pg/StartPay/{authority}"
            )

    elif provider == "snapppay":
        create_response = requests.get(
            "https://atropine.ir/kiani/Create.aspx",
            params={
                "amount": int(order.final_price),
                "userphone": student.user.mobile,
            }
        ).json()

        if not create_response.get("ok"):
            return JsonResponse(create_response, status=400)

        kiani_id = create_response["id"]

        payment_response = requests.get(
            "https://atropine.ir/kiani/SnappPay/Payment.aspx",
            params={
                "kianiId": kiani_id,
                "amount": int(order.final_price),
            }
        ).json()

        if not payment_response.get("ok"):
            return JsonResponse(payment_response, status=400)

        Payment.objects.create(
            order=order,
            amount=order.final_price,
            authority=str(kiani_id),
            provider=PaymentProvider.SNAPPPAY,
            kiani_id=kiani_id,
        )

        return redirect(payment_response["paymentPageUrl"])

    elif provider == "digipay":
        create_response = requests.get(
            "https://atropine.ir/kiani/Create.aspx",
            params={
                "amount": int(order.final_price),
                "userphone": student.user.mobile,
            }
        ).json()

        if not create_response.get("ok"):
            return JsonResponse(create_response, status=400)

        kiani_id = create_response["id"]

        payment_response = requests.get(
            "https://atropine.ir/kiani/DigiPay/Payment.aspx",
            params={
                "kianiId": kiani_id,
                "amount": int(order.final_price),
            }
        ).json()

        if not payment_response.get("ok"):
            return JsonResponse(payment_response, status=400)

        Payment.objects.create(
            order=order,
            amount=order.final_price,
            authority=str(kiani_id),
            provider=PaymentProvider.DIGIPAY,
            kiani_id=kiani_id,
        )

        return redirect(payment_response["paymentPageUrl"])
    else:
        return JsonResponse({"error": "درگاه نامعتبر است."}, status=400)

    if provider == "zarinpal":
        return JsonResponse(response)

    return JsonResponse(
        {"error": "خطا در ایجاد درخواست پرداخت."},
        status=400,
    )

def complete_payment(payment, ref_id=None):

    order = payment.order

    payment.status = PaymentStatus.SUCCESS
    payment.paid_at = timezone.now()

    if ref_id:
        payment.ref_id = str(ref_id)

    payment.save()

    order.paid = True
    order.save()

    # ثبت استفاده از کد تخفیف
    if order.discount_code:

        order.discount_code.usage_count += 1
        order.discount_code.save(update_fields=["usage_count"])

        DiscountUsage.objects.get_or_create(
            discount=order.discount_code,
            user=order.student.user,
            package_request=order,
        )

    # ثبت خدمات
    for service in order.package.service:

        ServiceToStudent.objects.get_or_create(
            student=order.student,
            service=service
        )

    try:
        requests.get(
            "https://atropine.ir/kiani/SMS/SendOrder.aspx",
            params={
                "phone": order.student.user.mobile,
                "basketId": order.package.id,
                "token": settings.KIANI_SMS_TOKEN,
            },
            timeout=10,
        )
    except Exception:
        pass

def verify_payment(request):

    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    payment = get_object_or_404(
        Payment,
        authority=authority
    )

    if status != "OK":

        payment.status = PaymentStatus.CANCELED
        payment.save()

        return redirect("payment_list")

    order = payment.order

    if order.discount_code:

        valid, error = order.discount_code.is_valid(
            order.student.user,
            order.package,
            order.package.total_price
        )

        if not valid:

            payment.status = PaymentStatus.FAILED
            payment.save()

            return redirect("payment_list")

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(order.final_price) * 10,
        "authority": authority,
    }

    response = requests.post(
        "https://payment.zarinpal.com/pg/v4/payment/verify.json",
        json=data
    )

    try:
        response = response.json()
    except Exception:
        return JsonResponse({
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "body": response.text,
        }, status=500)

    if response.get("data", {}).get("code") == 100:

        complete_payment(
            payment,
            response["data"]["ref_id"]
        )

        return redirect("payment_list")

    payment.status = PaymentStatus.FAILED
    payment.save()

    return redirect("payment_list")

@login_required
def verify_kiani_payment(request):

    payment = (
        Payment.objects.filter(
            order__student__user=request.user,
            provider__in=[
                PaymentProvider.SNAPPPAY,
                PaymentProvider.DIGIPAY,
            ],
            status=PaymentStatus.INIT,
        )
        .order_by("-created_at")
        .first()
    )

    if payment is None:
        return redirect("payment_list")

    response = requests.get(
        "https://atropine.ir/kiani/Get.aspx",
        params={
            "id": payment.kiani_id
        }
    ).json()

    if response.get("ok") and response.get("isPaid"):

        complete_payment(payment)

    else:

        payment.status = PaymentStatus.FAILED
        payment.save()

    return redirect("payment_list")

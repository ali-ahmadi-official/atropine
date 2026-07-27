import requests
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse

from .models import (
    Package,
    PackageRequest,
    Payment,
    PaymentStatus,
    ServiceToStudent,
    DiscountUsage,
)

def start_payment(request, package_id):

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

    student = request.user.user_student

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
            authority=authority
        )

        return redirect(
            f"https://payment.zarinpal.com/pg/StartPay/{authority}"
        )

    return JsonResponse(response)

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

    # دوباره اعتبار کد تخفیف
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

        payment.status = PaymentStatus.SUCCESS
        payment.ref_id = response["data"]["ref_id"]
        payment.paid_at = timezone.now()
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

        return redirect("payment_list")

    payment.status = PaymentStatus.FAILED
    payment.save()

    return redirect("payment_list")
import requests
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import ServiceToStudent, Package, PackageRequest, Payment, PaymentStatus

from django.views.decorators.http import require_GET

@require_GET
def start_payment(request, package_id):

    # 1. گرفتن پلن
    package = get_object_or_404(Package, id=package_id)

    # 2. گرفتن student
    student = request.user.user_student

    # 3. ساخت یا جلوگیری از تکرار سفارش
    order, created = PackageRequest.objects.get_or_create(
        student=student,
        package=package,
        paid=False
    )

    # 4. ساخت callback
    callback_url = request.build_absolute_uri(
        reverse("payment_verify")
    )

    # 5. درخواست زرین‌پال
    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(package.total_price) * 10,
        "description": f"پرداخت پکیج {package.id}",
        "callback_url": callback_url,
        "metadata": {
            "mobile": student.user.mobile
        }
    }

    response = requests.post(
        "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
        json=data
    ).json()

    if response["data"]["code"] == 100:

        authority = response["data"]["authority"]

        Payment.objects.create(
            order=order,
            amount=package.total_price,
            authority=authority
        )

        return JsonResponse({
            "url": f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
        })

    return JsonResponse(response)

from django.shortcuts import redirect

def verify_payment(request):

    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    payment = get_object_or_404(Payment, authority=authority)

    # ❌ اگر کاربر cancel کرد
    if status != "OK":
        payment.status = PaymentStatus.CANCELED
        payment.save()

        return (reverse("payment_list"))

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(payment.order.package.total_price) * 10,  # ریال
        "authority": authority
    }

    response = requests.post(
        "https://sandbox.zarinpal.com/pg/v4/payment/verify.json",
        json=data
    ).json()

    if response["data"]["code"] == 100:

        payment.status = PaymentStatus.SUCCESS
        payment.ref_id = response["data"]["ref_id"]
        payment.paid_at = timezone.now()
        payment.save()

        payment.order.paid = True
        payment.order.save()

        # services
        for service in payment.order.package.service:
            ServiceToStudent.objects.create(
                student=payment.order.student,
                service=service
            )

        return redirect(reverse("payment_list"))

    payment.status = PaymentStatus.FAILED
    payment.save()

    return redirect(reverse("payment_list"))
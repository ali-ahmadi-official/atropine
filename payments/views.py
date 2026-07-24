import requests

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET

from .models import (
    Package,
    PackageRequest,
    Payment,
    PaymentStatus,
    ServiceToStudent,
)


@require_GET
def start_payment(request, package_id):

    # بررسی لاگین بودن
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "ابتدا وارد حساب کاربری شوید."
        }, status=403)


    # فقط داوطلب اجازه خرید دارد
    if request.user.role != "student":
        return JsonResponse({
            "error": "فقط حساب داوطلب امکان خرید دارد."
        }, status=403)


    package = get_object_or_404(
        Package,
        id=package_id
    )


    try:
        student = request.user.user_student

    except Exception:
        return JsonResponse({
            "error": "حساب داوطلب برای این کاربر وجود ندارد."
        }, status=403)



    # پیدا کردن سفارش ساخته شده در payment_view
    order = get_object_or_404(
        PackageRequest,
        student=student,
        package=package,
        paid=False
    )


    # جلوگیری از پرداخت رایگان
    if order.final_price <= 0:

        return JsonResponse({
            "error": "این سفارش نیاز به پرداخت ندارد."
        }, status=400)



    callback_url = request.build_absolute_uri(
        reverse("payment_verify")
    )



    data = {

        "merchant_id": settings.ZARINPAL_MERCHANT_ID,

        # مبلغ به ریال
        "amount": int(order.final_price) * 10,

        "description":
            f"پرداخت پکیج {package.id}",

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


    authority = request.GET.get(
        "Authority"
    )

    status = request.GET.get(
        "Status"
    )



    payment = get_object_or_404(
        Payment,
        authority=authority
    )



    # کاربر پرداخت را لغو کرده
    if status != "OK":


        payment.status = PaymentStatus.CANCELED

        payment.save()


        return redirect(
            reverse("payment_list")
        )





    data = {


        "merchant_id":
            settings.ZARINPAL_MERCHANT_ID,


        # مبلغ سفارش نه پکیج
        "amount":
            int(payment.order.final_price) * 10,


        "authority":
            authority

    }



    response = requests.post(
        "https://payment.zarinpal.com/pg/v4/payment/verify.json",
        json=data
    ).json()





    if response.get("data", {}).get("code") == 100:


        payment.status = PaymentStatus.SUCCESS

        payment.ref_id = (
            response["data"]["ref_id"]
        )

        payment.paid_at = timezone.now()

        payment.save()



        order = payment.order

        order.paid = True

        order.save()



        # ثبت خدمات خریداری شده
        for service in order.package.service:


            ServiceToStudent.objects.get_or_create(

                student=order.student,

                service=service

            )



        return redirect(
            reverse("payment_list")
        )






    payment.status = PaymentStatus.FAILED

    payment.save()



    return redirect(
        reverse("payment_list")
    )
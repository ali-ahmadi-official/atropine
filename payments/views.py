import requests
import jdatetime
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.urls import reverse
from django.db import transaction
from accounts.models import User, Student, ConsultantSchedule
from .models import Consultation

from .models import (
    Package,
    PackageRequest,
    Payment,
    PaymentStatus,
    ServiceToStudent,
    DiscountUsage,
    PaymentProvider
)

def send_reserve_sms(phone, doctor, saat, tarikh):
    try:
        requests.get(
            "http://atropine.ir/kiani/SMS/SendReserve.aspx",
            params={
                "phone": phone,
                "doctor": doctor,
                "saat": saat,
                "tarikh": tarikh,
                "token": "tokenQeuykplnvnws",
            },
            timeout=10,
        )
    except Exception:
        pass

def send_doctor_sms(phone, saat, tarikh):
    try:
        requests.get(
            "http://atropine.ir/kiani/SMS/SendDoctor.aspx",
            params={
                "phone": phone,
                "saat": saat,
                "tarikh": tarikh,
                "token": "tokenQeuykplnvnws",
            },
            timeout=10,
        )
    except Exception:
        pass

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

    wallet = student.wallet

    wallet_amount = min(
        wallet.amount,
        order.final_price
    )

    gateway_amount = order.final_price - wallet_amount

    if gateway_amount < 0:
        return JsonResponse(
            {
                "error": "مبلغ پرداخت نامعتبر است."
            },
            status=400
        )

    if gateway_amount == 0:
        with transaction.atomic():

            payment = Payment.objects.create(
                order=order,
                amount=order.final_price,
                wallet_amount=wallet_amount,
                gateway_amount=0,
                authority=f"WALLET-{order.id}",
                provider=PaymentProvider.WALLET,
                status=PaymentStatus.SUCCESS,
            )

            complete_payment(payment)

            schedule_id = request.session.pop(
                "reserve_schedule_id",
                None
            )

            if schedule_id:
                auto_reserve(
                    schedule_id,
                    student
                )

        request.session["consultation_reserved"] = bool(schedule_id)
        request.session["payment_success"] = True

        return redirect("payment_list")

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
            "amount": int(gateway_amount) * 10,
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
                wallet_amount=wallet_amount,
            gateway_amount=gateway_amount,
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
                "amount": int(gateway_amount) * 10,
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
                "amount": int(gateway_amount) * 10,
            }
        ).json()

        if not payment_response.get("ok"):
            return JsonResponse(payment_response, status=400)

        Payment.objects.create(
            order=order,
            amount=order.final_price,
            wallet_amount=wallet_amount,
            gateway_amount=gateway_amount,
            authority=str(kiani_id),
            provider=PaymentProvider.SNAPPPAY,
            kiani_id=kiani_id,
        )

        return redirect(payment_response["paymentPageUrl"])

    elif provider == "digipay":
        create_response = requests.get(
            "https://atropine.ir/kiani/Create.aspx",
            params={
                "amount": int(gateway_amount) * 10,
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
                "amount": int(gateway_amount) * 10,
            }
        ).json()

        if not payment_response.get("ok"):
            return JsonResponse(payment_response, status=400)

        Payment.objects.create(
            order=order,
            amount=order.final_price,
            wallet_amount=wallet_amount,
            gateway_amount=gateway_amount,
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

    if payment.wallet_amount:

        wallet = order.student.wallet

        wallet.amount -= payment.wallet_amount

        wallet.save(update_fields=["amount"])

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

def auto_reserve(schedule_id, student):

    schedule = ConsultantSchedule.objects.filter(
        id=schedule_id,
        is_reserved=False
    ).first()

    schedule.date_shamsi = jdatetime.date.fromgregorian(
        date=schedule.date
    ).strftime("%Y/%m/%d")

    if schedule is None:
        return False

    if schedule.consultant.user.last_name == "نایب زاده":
        service_code = "1"
        doctor_name = "نایب‌زاده"
    else:
        service_code = "2"
        doctor_name = "جهان‌تیغ"

    service = ServiceToStudent.objects.filter(
        student=student,
        service=service_code,
        is_used=False
    ).first()

    if service is None:
        return False

    with transaction.atomic():

        service.is_used = True
        service.save(update_fields=["is_used"])

        schedule.is_reserved = True
        schedule.save(update_fields=["is_reserved"])

        Consultation.objects.create(
            service=service,
            schedule=schedule
        )
        
        tarikh = jdatetime.date.fromgregorian(
            date=schedule.date
        ).strftime("%Y%m%d")

        saat = schedule.time.strftime("%H")

        send_reserve_sms(
            phone=student.mobile,
            doctor=doctor_name,
            saat=saat,
            tarikh=tarikh,
        )

        send_doctor_sms(
            phone=schedule.consultant.user.mobile,
            saat=saat,
            tarikh=tarikh,
        )

    return True

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
        "amount": int(payment.gateway_amount) * 10,
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

        schedule_id = request.session.pop(
            "reserve_schedule_id",
            None
        )

        if schedule_id:
            auto_reserve(
                schedule_id,
                payment.order.student
            )

        request.session["consultation_reserved"] = bool(schedule_id)
        request.session["payment_success"] = True

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

        request.session["payment_success"] = True

        complete_payment(payment)

        schedule_id = request.session.pop(
            "reserve_schedule_id",
            None
        )

        if schedule_id:
            auto_reserve(
                schedule_id,
                payment.order.student
            )

        request.session["consultation_reserved"] = bool(schedule_id)

    else:

        payment.status = PaymentStatus.FAILED
        payment.save()

    return redirect("payment_list")

@require_GET
def check_pending_payments(request):

    # امنیت اجرای Cron
    if request.GET.get("token") != settings.PAYMENT_CRON_TOKEN:
        return JsonResponse(
            {"error": "Unauthorized"},
            status=403
        )

    # پرداخت‌های کمتر از 15 دقیقه را بررسی نکن
    cutoff = timezone.now() - timedelta(minutes=15)

    payments = Payment.objects.filter(
        status=PaymentStatus.INIT,
        created_at__lte=cutoff,
        provider__in=[
            PaymentProvider.ZARINPAL,
            PaymentProvider.SNAPPPAY,
            PaymentProvider.DIGIPAY,
        ],
    ).order_by("created_at")

    result = {
        "checked": 0,
        "success": 0,
        "pending": 0,
        "errors": 0,
    }

    for payment in payments:

        result["checked"] += 1

        try:

            # =========================
            # زرین پال
            # =========================
            if payment.provider == PaymentProvider.ZARINPAL:

                response = requests.post(
                    "https://payment.zarinpal.com/pg/v4/payment/verify.json",
                    json={
                        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
                        "amount": int(payment.gateway_amount) * 10,
                        "authority": payment.authority,
                    },
                    timeout=15,
                )

                data = response.json()

                if data.get("data", {}).get("code") == 100:

                    ref_id = data["data"].get("ref_id")

                    with transaction.atomic():

                        # جلوگیری از اجرای همزمان با callback
                        locked_payment = (
                            Payment.objects
                            .select_for_update()
                            .get(pk=payment.pk)
                        )

                        # اگر callback قبلاً پرداخت را تکمیل کرده
                        if locked_payment.status != PaymentStatus.INIT:
                            continue

                        complete_payment(
                            locked_payment,
                            ref_id=ref_id
                        )

                    result["success"] += 1

                else:
                    result["pending"] += 1

            # =========================
            # اسنپ پی / دیجی پی
            # =========================
            elif payment.provider in [
                PaymentProvider.SNAPPPAY,
                PaymentProvider.DIGIPAY,
            ]:

                if not payment.kiani_id:
                    continue

                response = requests.get(
                    "https://atropine.ir/kiani/Get.aspx",
                    params={
                        "id": payment.kiani_id
                    },
                    timeout=15,
                )

                data = response.json()

                if data.get("ok") and data.get("isPaid"):

                    with transaction.atomic():

                        locked_payment = (
                            Payment.objects
                            .select_for_update()
                            .get(pk=payment.pk)
                        )

                        # ممکن است همزمان callback پرداخت را تکمیل کرده باشد
                        if locked_payment.status != PaymentStatus.INIT:
                            continue

                        complete_payment(locked_payment)

                    result["success"] += 1

                else:
                    result["pending"] += 1

        except Exception:
            result["errors"] += 1

    return JsonResponse({
        "ok": True,
        **result
    })
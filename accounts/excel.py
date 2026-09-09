from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Max, Q
from payments.models import Consultation
from .models import Student, ConsultantSchedule

def export_form(request, id, form_attr, filename):
    from openpyxl import Workbook

    schedule = get_object_or_404(
        ConsultantSchedule,
        id=id,
        consultant=request.user.user_consultant,
    )

    consultation = get_object_or_404(
        Consultation.objects.select_related(
            "service__student"
        ),
        schedule=schedule,
    )

    student = consultation.service.student

    if not hasattr(student, form_attr):
        raise Http404("فرم مورد نظر تکمیل نشده است.")

    form = getattr(student, form_attr)

    wb = Workbook()
    ws = wb.active
    ws.title = filename.split(".")[0]

    # عنوان ستون‌ها
    ws["A1"] = "عنوان"
    ws["B1"] = "مقدار"

    row = 2

    for field in form._meta.fields:

        if field.name in ["id", "student"]:
            continue

        value = getattr(form, field.name)

        # حذف * از verbose_name
        label = field.verbose_name.replace("*", "")

        # اگر فایل بود فقط لینک/نام فایل ثبت شود
        if hasattr(value, "url"):
            value = request.build_absolute_uri(value.url)

        ws.cell(row=row, column=1).value = label
        ws.cell(row=row, column=2).value = str(value) if value is not None else ""

        row += 1

    # تنظیم عرض ستون‌ها
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 80

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{filename}"'

    wb.save(response)

    return response

def export_form1_excel(request, id):
    return export_form(
        request,
        id,
        "student_form_1",
        "student_form_1.xlsx",
    )

def export_form2_excel(request, id):
    return export_form(
        request,
        id,
        "student_form_2",
        "student_form_2.xlsx",
    )

def export_form3_excel(request, id):
    return export_form(
        request,
        id,
        "student_form_3",
        "student_form_3.xlsx",
    )

def export_students_excel(request):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment

    students = (
        Student.objects
        .filter(user__role="student")
        .select_related("user", "wallet")
        .annotate(
            services_count=Count(
                "student_to_services",
                distinct=True,
            ),
            consultations_count=Count(
                "student_to_services__consultation",
                distinct=True,
            ),
            held_consultations_count=Count(
                "student_to_services__consultation",
                filter=Q(
                    student_to_services__consultation__schedule__is_held=True
                ),
                distinct=True,
            ),
            reserved_consultations_count=Count(
                "student_to_services__consultation",
                filter=Q(
                    student_to_services__consultation__schedule__is_reserved=True
                ),
                distinct=True,
            ),
            packages_count=Count(
                "student_packege_requests",
                distinct=True,
            ),
            total_purchase=Sum(
                "student_packege_requests__final_price"
            ),
            last_purchase=Max(
                "student_packege_requests__created_at"
            ),
            successful_payment_amount=Sum(
                "student_packege_requests__order__amount",
                filter=Q(
                    student_packege_requests__order__status="SUCCESS"
                ),
            ),
            last_payment=Max(
                "student_packege_requests__order__paid_at",
                filter=Q(
                    student_packege_requests__order__status="SUCCESS"
                ),
            ),
        )
        .order_by("-id")
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "داوطلبان"

    headers = [
        "شناسه",
        "نام",
        "نام خانوادگی",
        "شماره موبایل",
        "نام کاربری",
        "تاریخ عضویت",

        "موجودی کیف پول",

        "تعداد خریدها",
        "مبلغ کل خریدها",
        "مبلغ پرداخت‌های موفق",
        "آخرین خرید",
        "آخرین پرداخت",

        "تعداد خدمات",
        "تعداد جلسات مشاوره",
        "جلسات رزرو شده",
        "جلسات برگزار شده",
    ]

    # Header
    for column, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=column, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Data
    for row, student in enumerate(students, start=2):
        user = student.user

        data = [
            student.id,
            user.first_name,
            user.last_name,
            user.mobile,
            user.username,
            user.date_joined.strftime("%Y-%m-%d %H:%M")
            if user.date_joined else "",

            student.wallet.amount if hasattr(student, "wallet") else 0,

            student.packages_count or 0,
            student.total_purchase or 0,
            student.successful_payment_amount or 0,

            student.last_purchase.strftime("%Y-%m-%d %H:%M")
            if student.last_purchase else "",

            student.last_payment.strftime("%Y-%m-%d %H:%M")
            if student.last_payment else "",

            student.services_count or 0,
            student.consultations_count or 0,
            student.reserved_consultations_count or 0,
            student.held_consultations_count or 0,
        ]

        for column, value in enumerate(data, start=1):
            ws.cell(
                row=row,
                column=column,
                value=value
            )

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="students.xlsx"'
    )

    wb.save(response)

    return response

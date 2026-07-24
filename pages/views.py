import os
import jdatetime
from collections import defaultdict
from datetime import timedelta, datetime
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from apps.models import ContentCategory
from accounts.models import User, Rank, ConsultantSchedule, Student
from accounts.forms import RankForm, AForm, Personality60Form
from payments.models import Package, ServiceToStudent, PackageRequest, Payment, Consultation
from .models import (
    Story, LiveEvent, Achievement, DataIntroduction, AboutUsIntroduction,
    PlansIntroduction, CounselingIntroduction, EstimationIntroduction, ChoiceIntroduction,
    Poster, Comment, FAQ, Media, RankBank, Rule, StaticMessage
)
from .forms import CompleteProfileForm

def main(request):
    stories = Story.objects.filter(show_in__icontains="main")

    now = timezone.now()
    a_live_is_active = LiveEvent.objects.filter(
        is_public=True,
        start_datetime__lte=now,
        end_datetime__gte=now
    ).first()

    next_live = LiveEvent.objects.filter(
        show_in__icontains="main",
        is_public=True,
        start_datetime__gte=now,
    ).first()

    if next_live:
        if next_live.start_datetime:
            next_live.start_datetime_shamsi = jdatetime.datetime.fromgregorian(
                datetime=next_live.start_datetime
            ).strftime("%Y/%m/%d %H:%M")
        else:
            next_live.start_datetime_shamsi = ""

    all_categories = list(ContentCategory.objects.all())
    chunk_size = 10
    categorized_list = [all_categories[i:i + chunk_size] for i in range(0, len(all_categories), chunk_size)]

    achievements = Achievement.objects.all()

    atropine_teams = User.objects.filter(role='consultant')

    posters = Poster.objects.filter(show_in__icontains="main")

    context = {
        'stories': stories,
        'a_live_is_active': a_live_is_active,
        'categorized_list': categorized_list,
        'achievements': achievements,
        'atropine_teams': atropine_teams,
        'next_live': next_live,
        'posters': posters,
    }

    return render(request, 'pages/main.html', context)

def compass(request):
    stories = Story.objects.filter(show_in__icontains="compass")

    now = timezone.now()
    a_live_is_active = LiveEvent.objects.filter(
        is_public=True,
        start_datetime__lte=now,
        end_datetime__gte=now
    ).first()

    posters = Poster.objects.filter(show_in__icontains="compass")

    lives = LiveEvent.objects.filter(
        show_in__icontains="compass",
        is_public=True,
    )

    for live in lives:
        if live.start_datetime:
            live.start_date_shamsi = jdatetime.date.fromgregorian(
                date=live.start_datetime.date()
            ).strftime("%Y/%m/%d")

            live.status = "برگزار شده" if live.start_datetime <= now else "آتی"
        else:
            live.start_date_shamsi = ""
            live.status = "-"

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    atropine_teams = User.objects.filter(role='consultant')

    comments = Comment.objects.all().order_by("-id")
    
    faqs = FAQ.objects.all().order_by("-id")

    context = {
        "stories": stories,
        "a_live_is_active": a_live_is_active,
        "posters": posters,
        "lives": lives,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
        "atropine_teams": atropine_teams,
        "comments": comments,
        "faqs": faqs,
    }

    return render(request, 'pages/compass.html', context)

def story_show(request, id, show):
    stories = Story.objects.filter(id__gte=id, show_in__icontains=show)
    story_data = []
    video_extensions = {
        '.mp4',
        '.webm',
        '.ogg',
        '.mov',
        '.m4v',
        '.avi',
        '.mkv'
    }

    for item in stories:
        ext = os.path.splitext(item.content.name)[1].lower()
        story_data.append({
            "name": item.title,
            "type": "video" if ext in video_extensions else "image",
            "src": item.content.url
        })

    context = {
        "stories": story_data
    }

    return render(request, "pages/story_show.html", context)

def self_story_show(request, id):
    stories = Story.objects.filter(id=id)
    story_data = []
    video_extensions = {
        '.mp4',
        '.webm',
        '.ogg',
        '.mov',
        '.m4v',
        '.avi',
        '.mkv'
    }

    for item in stories:
        ext = os.path.splitext(item.content.name)[1].lower()
        story_data.append({
            "name": item.title,
            "type": "video" if ext in video_extensions else "image",
            "src": item.content.url
        })

    context = {
        "stories": story_data
    }

    return render(request, "pages/story_show.html", context)

def courses(request):
    return render(request, 'pages/courses.html')

def plans(request):
    intro = PlansIntroduction.objects.last()
    try:
        rank_form = Rank.objects.filter(student=request.user.user_student).first()
    except:
        rank_form = None
    plans = Package.objects.all()

    context = {
        'intro': intro,
        'rank_form': rank_form,
        'plans': plans,
    }
    return render(request, 'pages/plans.html', context)

def counseling_introduction(request):
    intro = CounselingIntroduction.objects.last()
    consultants = User.objects.filter(role='consultant')

    context = {
        'intro': intro,
        'consultants': consultants,
    }
    return render(request, 'pages/counseling_introduction.html', context)

from collections import defaultdict
from datetime import timedelta

import jdatetime
from django.shortcuts import get_object_or_404, render
from django.utils import timezone


def consultant_show(request, id):

    consultant = get_object_or_404(
        User,
        role="consultant",
        id=id
    )

    schedules = (
        ConsultantSchedule.objects.filter(
            consultant__user=consultant
        )
        .order_by("date", "start_time")
    )

    # ------------------ شروع هفته جاری (شنبه) ------------------

    today = timezone.localdate()
    now = timezone.localtime()
    current_week_start = today - timedelta(days=(today.weekday() + 2) % 7)

    # ------------------ گروه بندی هفته ها ------------------

    week_dict = defaultdict(list)

    for schedule in schedules:

        week_start = schedule.date - timedelta(
            days=(schedule.date.weekday() + 2) % 7
        )

        week_dict[week_start].append(schedule)

    future_weeks = sorted(
        [w for w in week_dict.keys() if w >= current_week_start]
    )

    past_weeks = sorted(
        [w for w in week_dict.keys() if w < current_week_start]
    )

    ordered_weeks = future_weeks + past_weeks

    day_names = [
        "شنبه",
        "یکشنبه",
        "دوشنبه",
        "سه شنبه",
        "چهارشنبه",
        "پنجشنبه",
        "جمعه",
    ]

    weeks = []

    for week_start in ordered_weeks:

        # نوبت‌های هر روز
        days = []

        for i in range(7):

            day_date = week_start + timedelta(days=i)

            slots = sorted(
                [
                    s
                    for s in week_dict[week_start]
                    if s.date == day_date
                ],
                key=lambda x: x.start_time
            )

            days.append({
                "name": day_names[i],
                "date": day_date,
                "date_shamsi": jdatetime.date.fromgregorian(
                    date=day_date
                ).strftime("%Y/%m/%d"),
                "slots": slots,
            })

        # ساخت ماتریس جدول
        rows = []

        for row in range(15):

            row_data = []

            for day in days:

                if row < len(day["slots"]):

                    slot = day["slots"][row]

                    slot_datetime = timezone.make_aware(
                        datetime.combine(slot.date, slot.start_time)
                    )

                    slot.is_available = (
                        (not slot.is_reserved) and
                        (slot_datetime > now)
                    )

                    row_data.append(slot)

                else:

                    row_data.append(None)

            rows.append(row_data)

        weeks.append({

            "title": jdatetime.date.fromgregorian(
                date=week_start
            ).strftime("%Y/%m/%d"),

            "is_current": week_start == current_week_start,

            "days": days,

            "rows": rows,

        })

    context = {

        "consultant": consultant,

        "weeks": weeks,

    }

    return render(
        request,
        "pages/consultant_show.html",
        context,
    )

def estimation_introduction(request):
    intro = EstimationIntroduction.objects.last()

    context = {
        'intro': intro,
    }
    return render(request, 'pages/estimation_introduction.html', context)

def choice_introduction(request):
    intro = ChoiceIntroduction.objects.last()

    posters = Poster.objects.filter(show_in__icontains="choice")

    atropine_teams = User.objects.filter(role='consultant')

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        'intro': intro,
        'posters': posters,
        'atropine_teams': atropine_teams,
        'single_service_packages': single_service_packages,
        'multi_service_packages': multi_service_packages,
    }
    return render(request, 'pages/choice_introduction.html', context)

def live_introduction(request, id):
    live = get_object_or_404(LiveEvent, id=id)

    now = timezone.now()

    if live.start_datetime:
        live.start_date_shamsi = jdatetime.date.fromgregorian(
            date=live.start_datetime.date()
        ).strftime("%Y/%m/%d")

        live.status = "برگزار شده" if live.start_datetime <= now else "آتی"
    else:
        live.start_date_shamsi = ""
        live.status = "-"

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "live": live,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/live_introduction.html', context)

def live_time_steps(request):
    now = timezone.now()

    lives = LiveEvent.objects.filter(
        is_public=True,
    )

    for live in lives:
        if live.start_datetime:
            live.start_date_shamsi = jdatetime.date.fromgregorian(
                date=live.start_datetime.date()
            ).strftime("%Y/%m/%d")

            live.status = "برگزار شده" if live.start_datetime <= now else "آتی"
        else:
            live.start_date_shamsi = ""
            live.status = "-"

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "lives": lives,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/live_time_steps.html', context)

def live_archives(request):
    now = timezone.now()

    lives = LiveEvent.objects.filter(
        show_in__icontains="archives",
        is_public=True,
    )

    shamsi_years = sorted(
        lives.values_list("year", flat=True).distinct(),
        reverse=True,
    )

    categories = sorted(
        lives.exclude(category="")
            .values_list("category", flat=True)
            .distinct()
    )

    selected_year = request.GET.get("year")
    selected_category = request.GET.get("category")

    if selected_year:
        lives = lives.filter(year=selected_year)

    if selected_category:
            lives = lives.filter(category=selected_category)

    for live in lives:
        if live.start_datetime:
            live.start_date_shamsi = jdatetime.date.fromgregorian(
                date=live.start_datetime.date()
            ).strftime("%Y/%m/%d")

            live.status = "برگزار شده" if live.start_datetime <= now else "آتی"
        else:
            live.start_date_shamsi = ""
            live.status = "-"

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "lives": lives,
        "years": shamsi_years,
        "categories": categories,
        "selected_year": str(selected_year) if selected_year else "",
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }

    return render(request, "pages/live_archives.html", context)

def data_introduction(request, id):
    data_intro = get_object_or_404(DataIntroduction, id=id)

    posters = Poster.objects.filter(show_in__icontains="DataIntroduction")

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "data_intro": data_intro,
        "posters": posters,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/data_introduction.html', context)

def videos(request):
    medias = Media.objects.filter(media_type="video")
    is_paid = False
    
    if request.user.is_authenticated and request.user.role == "student":
    
        student = getattr(request.user, "user_student", None)
    
        if student:
    
            has_database_service = ServiceToStudent.objects.filter(
                student=student,
                service="5",
                is_used=False
            ).exists()
    
            if not has_database_service:
                medias = medias.filter(is_free=True)
            else:
                is_paid = True
    
        else:
            medias = medias.filter(is_free=True)
    
    else:
        medias = medias.filter(is_free=True)

    shamsi_years = sorted(
        medias.values_list("year", flat=True).distinct(),
        reverse=True,
    )
    categories = sorted(
        medias.exclude(category="")
            .values_list("category", flat=True)
            .distinct()
    )

    selected_year = request.GET.get("year")
    selected_category = request.GET.get("category")

    if selected_year:
        medias = medias.filter(year=selected_year)

    if selected_category:
        medias = medias.filter(category=selected_category)

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "is_paid": is_paid,
        "title": "ویدئوهای معرفی اختصاصی رشته ها",
        "shamsi_years": shamsi_years,
        "categories": categories,
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/videos.html', context)

def else_videos(request):
    medias = Media.objects.filter(media_type="else_video")
    is_paid = False

    if request.user.is_authenticated and request.user.role == "student":

        student = getattr(request.user, "user_student", None)

        if student:

            has_database_service = ServiceToStudent.objects.filter(
                student=student,
                service="5",
                is_used=False
            ).exists()

            if not has_database_service:
                medias = medias.filter(is_free=True)
            else:
                is_paid = True

        else:
            medias = medias.filter(is_free=True)

    else:
        medias = medias.filter(is_free=True)

    shamsi_years = sorted(
        medias.values_list("year", flat=True).distinct(),
        reverse=True,
    )
    categories = sorted(
        medias.exclude(category="")
            .values_list("category", flat=True)
            .distinct()
    )

    selected_year = request.GET.get("year")
    selected_category = request.GET.get("category")

    if selected_year:
        medias = medias.filter(year=selected_year)

    if selected_category:
        medias = medias.filter(category=selected_category)

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "is_paid": is_paid,
        "title": "سایر ویدئوها",
        "shamsi_years": shamsi_years,
        "categories": categories,
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/videos.html', context)

def voices(request):
    medias = Media.objects.filter(media_type="voice")
    is_paid = False

    if request.user.is_authenticated and request.user.role == "student":

        student = getattr(request.user, "user_student", None)

        if student:

            has_database_service = ServiceToStudent.objects.filter(
                student=student,
                service="5",
                is_used=False
            ).exists()

            if not has_database_service:
                medias = medias.filter(is_free=True)
            else:
                is_paid = True

        else:
            medias = medias.filter(is_free=True)

    else:
        medias = medias.filter(is_free=True)

    shamsi_years = sorted(
        medias.values_list("year", flat=True).distinct(),
        reverse=True,
    )
    categories = sorted(
        medias.exclude(category="")
            .values_list("category", flat=True)
            .distinct()
    )

    selected_year = request.GET.get("year")
    selected_category = request.GET.get("category")

    if selected_year:
        medias = medias.filter(year=selected_year)

    if selected_category:
        medias = medias.filter(category=selected_category)

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "is_paid": is_paid,
        "title": "ویس های بررسی رشته شهرها",
        "shamsi_years": shamsi_years,
        "categories": categories,
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/voice.html', context)

def else_voices(request):
    medias = Media.objects.filter(media_type="else_voice")
    is_paid = False

    if request.user.is_authenticated and request.user.role == "student":
    
        student = getattr(request.user, "user_student", None)
    
        if student:
    
            has_database_service = ServiceToStudent.objects.filter(
                student=student,
                service="5",
                is_used=False
            ).exists()
    
            if not has_database_service:
                medias = medias.filter(is_free=True)
            else:
                is_paid = True
    
        else:
            medias = medias.filter(is_free=True)
    
    else:
        medias = medias.filter(is_free=True)

    shamsi_years = sorted(
        medias.values_list("year", flat=True).distinct(),
        reverse=True,
    )
    categories = sorted(
        medias.exclude(category="")
            .values_list("category", flat=True)
            .distinct()
    )

    selected_year = request.GET.get("year")
    selected_category = request.GET.get("category")

    if selected_year:
        medias = medias.filter(year=selected_year)

    if selected_category:
        medias = medias.filter(category=selected_category)

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "is_paid": is_paid,
        "title": "سایر ویس ها",
        "shamsi_years": shamsi_years,
        "categories": categories,
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/voice.html', context)

def rank_bank(request):
    ranks = RankBank.objects.all()

    is_paid = False
    
    if request.user.is_authenticated and request.user.role == "student":
    
        student = getattr(request.user, "user_student", None)
    
        if student:
    
            has_database_service = ServiceToStudent.objects.filter(
                student=student,
                service="5",
                is_used=False
            ).exists()
    
            if not has_database_service:
                ranks = ranks.filter(is_free=True)
            else:
                is_paid = True
    
        else:
            ranks = ranks.filter(is_free=True)
    
    else:
        ranks = ranks.filter(is_free=True)

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "is_paid": is_paid,
        "title": "بانک رتبه قبولی",
        "ranks": ranks,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/rank_bank.html', context)

def rule(request):
    rules = Rule.objects.all()

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "title": "قوانین و آئین نامه ها",
        "rules": rules,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/rule.html', context)

def rule_introduction(request, id):
    rule = get_object_or_404(Rule, id=id)

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "title": "قوانین و آئین نامه ها",
        "rule": rule,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/rule_introduction.html', context)

def static_message(request):
    static_messages = StaticMessage.objects.all()

    packages = Package.objects.all()

    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]

    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "title": "پاسخ به پرسش های داوطلبین",
        "static_messages": static_messages,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/static_message.html', context)

def about_us(request):
    intro = AboutUsIntroduction.objects.last()
    posters = Poster.objects.filter(show_in__icontains="AboutUsIntroduction")


    return render(request, 'pages/about_us.html', {"intro": intro, "posters": posters})

def trust(request):
    return render(request, 'pages/trust.html')

def achievement_list(request):
    achievements = Achievement.objects.all()

    return render(request, 'pages/achievement_list.html', {"achievements": achievements})

def atropine_team(request):
    atropine_teams = User.objects.filter(role='consultant')

    return render(request, 'pages/atropine_team.html', {"atropine_teams": atropine_teams})

def payment_view(request, package_id):

    package = get_object_or_404(Package, id=package_id)

    packages = Package.objects.all()
    
    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]
    
    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    context = {
        "package": package,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }

    # -----------------------
    # مرحله 1 : لاگین
    # -----------------------

    if not request.user.is_authenticated:

        context["need_login"] = True
        context["login_url"] = reverse("login")

        return render(request, "pages/payment.html", context)

    # -----------------------
    # مرحله 2 : تکمیل اطلاعات
    # -----------------------

    user = request.user

    if not user.first_name or not user.last_name or not user.mobile:

        if request.method == "POST":

            form = CompleteProfileForm(request.POST)

            if form.is_valid():

                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.mobile = form.cleaned_data["mobile"]
                user.save()

                return redirect(
                    reverse("payment_view", kwargs={"package_id": package.id})
                )

        else:

            form = CompleteProfileForm(
                initial={
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "mobile": user.mobile,
                }
            )

        context["profile_form"] = form

        return render(request, "pages/payment.html", context)

    # -----------------------
    # مرحله 3 : محاسبه مبلغ
    # -----------------------

    try:
        student = request.user.user_student
    except Student.DoesNotExist:
        context["only_student"] = True
        return render(request, "pages/payment.html", context)

    final_price = Decimal(package.total_price)
    discount = Decimal("0")

    owned_services = set(
        ServiceToStudent.objects.filter(
            student=student,
            is_used=False
        ).values_list("service", flat=True)
    )

    duplicate_services = []

    for service in package.service:

        if service not in owned_services:
            continue

        duplicate_services.append(service)

        single_package = None

        for p in Package.objects.filter(service__contains=service):
            if len(p.service) == 1 and p.service[0] == service:
                single_package = p
                break

        if single_package:
            discount += Decimal(single_package.total_price)

    service_choices = dict(Package.SERVICE_CHOICES)

    duplicate_service_labels = [
        service_choices.get(service)
        for service in duplicate_services
    ]

    final_price -= discount

    if final_price < 0:
        final_price = Decimal("0")

    order, created = PackageRequest.objects.get_or_create(
        student=student,
        package=package,
        paid=False,
        defaults={
            "final_price": final_price,
        }
    )

    if not created:
        order.final_price = final_price
        order.save(update_fields=["final_price"])

    context.update({
        "order": order,
        "duplicate_services": duplicate_services,
        "duplicate_service_labels": duplicate_service_labels,
        "discount": discount,
        "final_price": final_price,
        "can_pay": final_price > 0,
        "payment_url": reverse(
            "payment_start",
            kwargs={"package_id": package.id}
        ),
    })

    return render(request, "pages/payment.html", context)

@login_required
def payment_list(request):
    packages = Package.objects.all()
    
    single_service_packages = [
        p for p in packages
        if len(p.service) == 1
    ]
    
    multi_service_packages = [
        p for p in packages
        if len(p.service) != 1
    ]

    payments = Payment.objects.filter(
        order__student__user=request.user
    ).select_related(
        "order",
        "order__package"
    ).order_by(
        "-created_at"
    )


    last_payment = payments.first()


    context = {

        "single_service_packages": single_service_packages,

        "multi_service_packages": multi_service_packages,

        "payments": payments,

        "last_payment": last_payment,

    }


    return render(
        request,
        "pages/payment_list.html",
        context
    )

@login_required
def reserve_consultation(request, schedule_id):

    schedule = get_object_or_404(
        ConsultantSchedule,
        id=schedule_id,
        is_reserved=False
    )

    schedule.date_shamsi = jdatetime.date.fromgregorian(
        date=schedule.date
    ).strftime("%Y/%m/%d")

    consultant = schedule.consultant.user

    context = {
        "schedule": schedule,
        "consultant": consultant,
    }

    # فقط داوطلب
    if request.user.role != "student":
        context["student_required"] = True
        return render(request, "pages/reserve_consultation.html", context)

    student = request.user.user_student

    # تعیین نوع خدمت
    if consultant.last_name == "نایب زاده":
        service_code = "1"
        service_name = "جلسه فردی با دکتر نایب زاده"
    else:
        service_code = "2"
        service_name = "جلسه فردی با مشاور"

    context["service_name"] = service_name

    # خدمت خریداری شده
    service = ServiceToStudent.objects.filter(
        student=student,
        service=service_code,
        is_used=False
    ).first()

    if service is None:
        context["service_required"] = True
        return render(request, "pages/reserve_consultation.html", context)

    # ---------------------- Rank ----------------------

    if not hasattr(student, "student_rank"):

        if request.method == "POST" and request.POST.get("step") == "rank":

            form = RankForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():
                obj = form.save(commit=False)
                obj.student = student
                obj.save()

                return redirect(
                    "reserve_consultation",
                    schedule.id
                )

        else:
            form = RankForm()

        context["show_rank_form"] = True
        context["rank_form"] = form

        return render(request, "pages/reserve_consultation.html", context)

    # ---------------------- AB ----------------------

    if not (student.a_completed):

        if request.method == "POST" and request.POST.get("step") == "ab":

            form = AForm(request.POST)

            if form.is_valid():

                obj = form.save(commit=False)
                obj.student = student
                obj.save()

                obj.a_save()

                return redirect(
                    "reserve_consultation",
                    schedule.id
                )

        else:
            form = AForm()

        context["show_ab_form"] = True
        context["ab_form"] = form

        return render(request, "pages/reserve_consultation.html", context)

    # ---------------------- Personality ----------------------

    if not hasattr(student, "student_personality_60"):

        if request.method == "POST" and request.POST.get("step") == "personality":

            form = Personality60Form(request.POST)

            if form.is_valid():

                obj = form.save(commit=False)
                obj.student = student
                obj.save()

                return redirect(
                    "reserve_consultation",
                    schedule.id
                )

        else:
            form = Personality60Form()

        context["show_personality_form"] = True
        context["personality_form"] = form

        return render(request, "pages/reserve_consultation.html", context)

    # ---------------------- تایید نهایی ----------------------

    if request.method == "POST" and request.POST.get("step") == "confirm":

        with transaction.atomic():

            service.is_used = True
            service.save(update_fields=["is_used"])

            schedule.is_reserved = True
            schedule.save(update_fields=["is_reserved"])

            Consultation.objects.create(
                service=service,
                schedule=schedule
            )

        return redirect("student_consultations")

    context["ready_to_reserve"] = True

    return render(
        request,
        "pages/reserve_consultation.html",
        context
    )

@login_required
def student_consultations(request):

    context = {}

    # فقط داوطلب
    if request.user.role != "student":
        context["student_required"] = True
        return render(
            request,
            "pages/student_consultations.html",
            context
        )

    student = request.user.user_student

    consultations = (
        Consultation.objects
        .filter(service__student=student)
        .select_related(
            "service",
            "schedule",
            "schedule__consultant__user"
        )
        .order_by("-schedule__date", "-schedule__start_time")
    )

    for consultation in consultations:

        consultation.date_shamsi = jdatetime.date.fromgregorian(
            date=consultation.schedule.date
        ).strftime("%Y/%m/%d")

        consultation.consultant = (
            consultation.schedule.consultant.user
        )

    context["consultations"] = consultations
    context["today"] = timezone.localdate()

    return render(
        request,
        "pages/student_consultations.html",
        context
    )
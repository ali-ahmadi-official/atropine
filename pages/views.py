import os
import jdatetime
from datetime import datetime, time
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from apps.models import ContentCategory
from accounts.models import User, Rank, ConsultantSchedule, Student
from payments.models import Package
from .models import (
    Story, LiveEvent, Achievement, DataIntroduction, AboutUsIntroduction,
    PlansIntroduction, CounselingIntroduction, EstimationIntroduction, ChoiceIntroduction,
    Poster, Comment, FAQ, Media, RankBank, Rule, StaticMessage
)

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

def consultant_show(request, id):
    consultant = get_object_or_404(User, role='consultant', id=id)
    student_count = Student.objects.filter(
        student_packege_requests__paid=True,
        student_packege_requests__request_consultation__schedule__consultant__user=request.user
    ).distinct().count()
    

    now = timezone.localtime()

    schedules = ConsultantSchedule.objects.filter(
        consultant__user=consultant
    ).filter(
        Q(date__gt=now.date()) |
        Q(date=now.date(), end_time__gte=now.time())
    ).order_by("date", "start_time")

    for schedule in schedules:
        if schedule:
            schedule.date_shamsi = jdatetime.date.fromgregorian(
                date=schedule.date
            ).strftime('%Y/%m/%d')

    context = {
        'consultant': consultant,
        'student_count': student_count,
        'schedules': schedules,
    }
    return render(request, 'pages/consultant_show.html', context)

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

    selected_year = request.GET.get("year")

    if selected_year:
        lives = lives.filter(year=selected_year)

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

    shamsi_years = sorted(
        medias.values_list("year", flat=True).distinct(),
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
        medias = medias.filter(year=selected_year)

    if selected_category:
        lives = lives.filter(category=selected_category)

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
        "title": "سایر ویدئوها",
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/videos.html', context)

def voices(request):
    medias = Media.objects.filter(media_type="voice")

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
        "title": "ویس های بررسی رشته شهرها",
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/voice.html', context)

def else_voices(request):
    medias = Media.objects.filter(media_type="else_voice")

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
        "title": "سایر ویس ها",
        "medias": medias,
        "single_service_packages": single_service_packages,
        "multi_service_packages": multi_service_packages,
    }
    return render(request, 'pages/voice.html', context)

def rank_bank(request):
    ranks = RankBank.objects.all()

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

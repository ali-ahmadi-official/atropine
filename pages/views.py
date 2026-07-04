import os
import jdatetime
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from apps.models import ContentCategory
from accounts.models import User, Rank, ConsultantSchedule, Student
from payments.models import Package
from .models import (
    Story, LiveEvent, Achievement,
    PlansIntroduction, CounselingIntroduction, EstimationIntroduction, ChoiceIntroduction, LiveIntroduction
)

def main(request):
    stories = Story.objects.all()

    now = timezone.now()
    a_live_is_active = LiveEvent.objects.filter(
        is_public=True,
        start_datetime__lte=now,
        end_datetime__gte=now
    ).first()

    next_live = LiveEvent.objects.filter(
        is_public=True,
        start_datetime__gte=now,
    ).first()

    if next_live:
        next_live.start_datetime_shamsi = jdatetime.datetime.fromgregorian(
            datetime=next_live.start_datetime
        ).strftime('%Y/%m/%d %H:%M')

    all_categories = list(ContentCategory.objects.all())
    chunk_size = 10
    categorized_list = [all_categories[i:i + chunk_size] for i in range(0, len(all_categories), chunk_size)]

    achievements = Achievement.objects.all()

    atropine_teams = User.objects.exclude(role='student')

    context = {
        'stories': stories,
        'a_live_is_active': a_live_is_active,
        'categorized_list': categorized_list,
        'achievements': achievements,
        'atropine_teams': atropine_teams,
        'next_live': next_live,
    }

    return render(request, 'pages/main.html', context)

def story_show(request, id):
    stories = Story.objects.filter(id__gte=id)
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

    context = {
        'intro': intro,
    }
    return render(request, 'pages/choice_introduction.html', context)

def live_introduction(request):
    intro = LiveIntroduction.objects.last()

    now = timezone.now()
    next_lives = LiveEvent.objects.filter(
        is_public=True,
        end_datetime__gte=now,
    )

    for next_live in next_lives:
        if next_live:
            next_live.start_datetime_shamsi = jdatetime.datetime.fromgregorian(
                datetime=next_live.start_datetime
            ).strftime('%Y/%m/%d %H:%M')

    context = {
        'intro': intro,
        'next_lives': next_lives,
    }
    return render(request, 'pages/live_introduction.html', context)

def about_us(request):
    return render(request, 'pages/about_us.html')

def trust(request):
    return render(request, 'pages/trust.html')

def achievement_list(request):
    achievements = Achievement.objects.all()

    return render(request, 'pages/achievement_list.html', {"achievements": achievements})

def atropine_team(request):
    atropine_teams = User.objects.exclude(role='student')

    return render(request, 'pages/atropine_team.html', {"atropine_teams": atropine_teams})

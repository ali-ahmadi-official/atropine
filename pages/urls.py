from django.urls import path
from .views import (
    main, compass, story_show, self_story_show, courses, plans, data_introduction,
    counseling_introduction, consultant_show, estimation_introduction, choice_introduction,
    live_introduction, live_time_steps, live_archives,
    videos, else_videos, voices, else_voices, rank_bank, rule, rule_introduction, static_message,
    about_us, trust, achievement_list, atropine_team
)

urlpatterns = [
    path('', main, name='main'),
    path('compass/', compass, name='compass'),
    path('story-show/<int:id>/<slug:show>/', story_show, name='story_show'),
    path('self-story-show/<int:id>/', self_story_show, name='self_story_show'),
    path('courses/', courses, name='courses'),
    path('plans/', plans, name='plans'),
    path('plans/counseling-introduction/', counseling_introduction, name='counseling_introduction'),
    path('plans/consultant-show/<int:id>/', consultant_show, name='consultant_show'),
    path('plans/estimation-introduction/', estimation_introduction, name='estimation_introduction'),
    path('choice-introduction/', choice_introduction, name='choice_introduction'),
    path('data-introduction/<int:id>/', data_introduction, name='data_introduction'),
    path('live-introduction/<int:id>/', live_introduction, name='live_introduction'),
    path('live-time-steps/', live_time_steps, name='live_time_steps'),
    path('live-archives/', live_archives, name='live_archives'),
    path('videos/', videos, name='videos'),
    path('else-videos/', else_videos, name='else_videos'),
    path('voices/', voices, name='voices'),
    path('else-voices/', else_voices, name='else_voices'),
    path('rank-bank/', rank_bank, name='rank_bank'),
    path('rule/', rule, name='rule'),
    path('rule-introduction/<int:id>/', rule_introduction, name='rule_introduction'),
    path('static-message/', static_message, name='static_message'),
    path('about-us/', about_us, name='about_us'),
    path('trust/', trust, name='trust'),
    path('achievement-list/', achievement_list, name='achievement_list_show'),
    path('atropine-team/', atropine_team, name='atropine_team'),
]

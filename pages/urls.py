from django.urls import path
from .views import (
    main, compass, story_show, courses, plans,
    counseling_introduction, consultant_show, estimation_introduction, choice_introduction, live_introduction, 
    about_us, trust, achievement_list, atropine_team
)

urlpatterns = [
    path('', main, name='main'),
    path('compass/', compass, name='compass'),
    path('story-show/<int:id>/', story_show, name='story_show'),
    path('courses/', courses, name='courses'),
    path('plans/', plans, name='plans'),
    path('plans/counseling-introduction/', counseling_introduction, name='counseling_introduction'),
    path('plans/consultant-show/<int:id>/', consultant_show, name='consultant_show'),
    path('plans/estimation-introduction/', estimation_introduction, name='estimation_introduction'),
    path('plans/choice-introduction/', choice_introduction, name='choice_introduction'),
    path('plans/live-introduction/', live_introduction, name='live_introduction'),
    path('about-us/', about_us, name='about_us'),
    path('trust/', trust, name='trust'),
    path('achievement-list/', achievement_list, name='achievement_list_show'),
    path('atropine-team/', atropine_team, name='atropine_team'),
]

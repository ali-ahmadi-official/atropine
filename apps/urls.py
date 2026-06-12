from django.urls import path
from .views import (
    main, sign_in, forgot_password, otp, reset_password,
    search, my_course, wishlist, instructor, courses, onboarding,
    chat, chat_list
)

urlpatterns = [
    path('', onboarding, name='onboarding'),

    path('registrations/sign-in/', sign_in, name='sign_in'),
    path('registrations/forgot-password/', forgot_password, name='forgot_password'),
    path('registrations/otp/', otp, name='otp'),
    path('registrations/reset-password/', reset_password, name='reset_password'),

    path('index/', main, name='main'),
    path('search/', search, name='search'),
    path('my-course/', my_course, name='my_course'),
    path('wishlist/', wishlist, name='wishlist'),
    path('instructor/', instructor, name='instructor'),
    path('courses/', courses, name='courses'),

    path('chat/', chat, name='chat'),
    path('chat_list/', chat_list, name='chat_list'),
]

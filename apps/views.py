from django.shortcuts import render

def onboarding(request):
    return render(request, 'pages/onboarding.html')

def main(request):
    return render(request, 'pages/main.html')

def sign_in(request):
    return render(request, 'registrations/sign_in.html')

def forgot_password(request):
    return render(request, 'registrations/forgot_password.html')

def otp(request):
    return render(request, 'registrations/otp.html')

def reset_password(request):
    return render(request, 'registrations/reset_password.html')

def search(request):
    return render(request, 'pages/search.html')

def my_course(request):
    return render(request, 'pages/my_course.html')

def wishlist(request):
    return render(request, 'pages/wishlist.html')

def instructor(request):
    return render(request, 'pages/instructor.html')

def courses(request):
    return render(request, 'pages/courses.html')

def chat(request):
    return render(request, 'chats/chat.html')

def chat_list(request):
    return render(request, 'chats/chat_list.html')
import re
import jdatetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pages.models import (
    Story, Achievement, LiveEvent, Poster, Comment, FAQ,
    PlansIntroduction, CounselingIntroduction, EstimationIntroduction, DataIntroduction,
    ChoiceIntroduction, LiveIntroduction, AboutUsIntroduction, Media, RankBank, Rule, StaticMessage
)
from payments.models import Package, Consultation, Payment, ServiceToStudent
from .models import User, Student, Consultant, ConsultantSchedule, Rank, OTP, AB, Personality60
from .forms import (
    UserForm, UserCreationForm, StoryForm, AchievementForm, LiveEventForm, PosterForm, ConsultantForm, CreateConsultantForm, ConsultantScheduleForm,
    PackageForm, AForm, RankForm, Personality60Form,
    PlansIntroductionForm, CounselingIntroductionForm, EstimationIntroductionForm, DataIntroductionForm,
    ChoiceIntroductionForm, LiveIntroductionForm,
    AboutUsIntroductionForm, CommentForm, FAQForm, MediaForm, RankBankForm, RuleForm, StaticMessageForm
)
from .utils import generate_code, send_sms
from .personality.traits import calculate_item_scores
from .personality.personality import detect_personality_type, calculate_specialty_scores, apply_personal_modifier, categorize_specialties
from .personality.modifiers.personal import personal_modifier
from .validity.validiy import VALIDITY
from .validity.field_capacity import FIELD
from .validity.university_capacity import UNIVERSITY
from .validity.underutilized_capacity import UNDERUTILIZED
from .validity.calculator import AdmissionPredictor
from .mixins import SuperAdminSidebarContextMixin

def validate_mobile(mobile):
    mobile = mobile.strip()
    mobile = mobile.replace(" ", "").replace("-", "")

    if mobile.startswith("+98"):
        mobile = "0" + mobile[3:]

    elif mobile.startswith("98"):
        mobile = "0" + mobile[2:]

    pattern = r"^09\d{9}$"

    if not re.fullmatch(pattern, mobile):
        return False, None

    return True, mobile

def register(request):
    if request.method == "POST":

        mobile = request.POST.get("mobile", "").strip()

        if not mobile:
            messages.error(request, "شماره موبایل را وارد کنید.")
            return redirect("register")
        
        is_valid, mobile = validate_mobile(mobile)

        if not is_valid:
            messages.error(request, "شماره موبایل معتبر نیست.")
            return redirect("register")

        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, "این شماره موبایل قبلاً ثبت شده است.")
            return redirect("register")

        last_otp = OTP.objects.filter(
            mobile=mobile,
            is_used=False
        ).last()

        if last_otp and last_otp.is_valid():
            messages.warning(
                request,
                "کد قبلاً ارسال شده است. لطفاً تا پایان زمان اعتبار صبر کنید."
            )
            request.session["register_mobile"] = mobile
            return redirect("verify-register")

        code = generate_code()

        OTP.objects.create(
            mobile=mobile,
            code=code
        )

        send_sms(mobile, code)

        request.session["register_mobile"] = mobile

        return redirect("verify-register")

    return render(request, "accounts/register.html")

def verify_register(request):

    mobile = request.session.get("register_mobile")

    if not mobile:
        return redirect("register")

    if request.method == "POST":

        code = request.POST.get("code", "").strip()

        otp = OTP.objects.filter(
            mobile=mobile,
            code=code,
            is_used=False
        ).last()

        if otp is None:
            messages.error(request, "کد وارد شده صحیح نیست.")
            return redirect("verify-register")

        if not otp.is_valid():
            messages.error(request, "زمان اعتبار کد به پایان رسیده است.")
            return redirect("register")

        otp.is_used = True
        otp.save()

        request.session["verified_mobile"] = mobile

        return redirect("set-password")

    otp = OTP.objects.filter(
        mobile=mobile,
        is_used=False
    ).last()

    return render(request,
        "accounts/verify_register.html",
        {
            "otp": otp,
            'mobile': mobile
        }
    )

def set_password(request):

    mobile = request.session.get("verified_mobile")

    if not mobile:
        return redirect("register")

    if request.method == "POST":

        password = request.POST.get("password")

        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیستند.")
            return redirect("set-password")

        new_user = User.objects.create(
            username=mobile,
            mobile=mobile,
            password=make_password(password),
            role="student"
        )

        Student.objects.create(user=new_user)

        request.session.flush()

        return redirect("login")

    return render(request, "accounts/set_password.html")

def login_view(request):

    if request.method=="POST":

        username=request.POST["username"]
        password=request.POST["password"]

        user=authenticate(
            username=username,
            password=password
        )

        if user:
            login(request,user)
            if not user.first_name or not user.last_name:
                return redirect("complete-profile")
            
            if user.role == "super_admin":
                return redirect("admin_dashboard")

            elif user.role == "supervisor":
                return redirect("supervisor_dashboard")

            elif user.role == "consultant":
                return redirect("consultant_dashboard")

            elif user.role == "student":
                return redirect("main")

            return redirect("main")
        else:
            messages.error(request, "نام کاربری یا رمز عبور صحیح نیست.")
            return redirect("login")

    return render(request,"accounts/login.html")

def otp_login(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile", "").strip()

        if not mobile:
            messages.error(request, "شماره موبایل را وارد کنید.")
            return redirect("otp-login")
        
        is_valid, mobile = validate_mobile(mobile)

        if not is_valid:
            messages.error(request, "شماره موبایل معتبر نیست.")
            return redirect("otp-login")

        try:
            user = User.objects.get(mobile=mobile)

            if user.is_suspended:
                messages.error(request, "حساب کاربری شما تعلیق شده است.")
                return redirect("otp-login")

        except User.DoesNotExist:
            messages.error(request, "کاربری با این شماره موبایل وجود ندارد.")
            return redirect("otp-login")

        last_otp = OTP.objects.filter(
            mobile=mobile,
            is_used=False
        ).last()

        if last_otp and last_otp.is_valid():
            request.session["otp_mobile"] = mobile
            messages.warning(
                request,
                "کد قبلاً ارسال شده است."
            )
            return redirect("otp-verify")

        code = generate_code()

        OTP.objects.create(
            mobile=mobile,
            code=code
        )

        send_sms(mobile, code)

        request.session["otp_mobile"] = mobile

        return redirect("otp-verify")

    return render(request, "accounts/otp_login.html")

def otp_verify(request):

    mobile = request.session.get("otp_mobile")

    if not mobile:
        return redirect("otp-login")

    otp = OTP.objects.filter(
        mobile=mobile,
        is_used=False
    ).last()

    if otp is None:
        messages.error(request, "ابتدا درخواست کد ورود بدهید.")
        return redirect("otp-login")

    if request.method == "POST":

        code = request.POST.get("code", "").strip()

        if code != code:
            messages.error(request, "کد وارد شده صحیح نیست.")
            return redirect("otp-verify")

        if not otp.is_valid():
            messages.error(request, "زمان اعتبار کد به پایان رسیده است.")
            return redirect("otp-login")

        otp.is_used = True
        otp.save()

        user = User.objects.get(mobile=mobile)

        login(request, user)

        request.session.pop("otp_mobile", None)

        if not user.first_name or not user.last_name:
            return redirect("complete-profile")
        
        if user.role == "super_admin":
            return redirect("admin_dashboard")

        elif user.role == "supervisor":
            return redirect("supervisor_dashboard")

        elif user.role == "consultant":
            return redirect("consultant_dashboard")

        elif user.role == "student":
            return redirect("main")

        return redirect("main")

    return render(
        request,
        "accounts/otp_verify.html",
        {
            "otp": otp,
            "mobile": mobile,
        }
    )

@login_required
def complete_profile(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if not first_name or not last_name:
            messages.error(request, "نام و نام خانوادگی الزامی است.")
            return redirect("complete-profile")

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        if request.user.role == "super_admin":
            return redirect("admin_dashboard")

        elif request.user.role == "supervisor":
            return redirect("supervisor_dashboard")

        elif request.user.role == "consultant":
            return redirect("consultant_dashboard")

        elif request.user.role == "student":
            return redirect("main")

        return redirect("main")

    return render(request, "accounts/complete_profile.html")

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')

class MainLogoutView(LogoutView):
    next_page = reverse_lazy('main')

# region admin

def aside_super_admin_context():
    return {
        "PlansIntroductionCreated": PlansIntroduction.objects.first(),
        "CounselingIntroductionCreated": CounselingIntroduction.objects.first(),
        "EstimationIntroductionCreated": EstimationIntroduction.objects.first(),
        "ChoiceIntroductionCreated": ChoiceIntroduction.objects.first(),
        "LiveIntroductionCreated": LiveIntroduction.objects.first(),
        "AboutUsIntroductionCreated": AboutUsIntroduction.objects.first(),
        "DataIntroductionCreated": DataIntroduction.objects.first(),
    }

def admin_dashboard(request):
    aside = aside_super_admin_context()
    return render(request, "accounts/admins/dashboard.html", aside)

class UserListView(SuperAdminSidebarContextMixin, ListView):
    model = User
    template_name = "accounts/admins/user_list.html"
    context_object_name = "users"

class UserCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "accounts/admins/user_add.html"
    success_url = reverse_lazy("user_list")

class UserUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "accounts/admins/user_edit.html"
    success_url = reverse_lazy("user_list")

class UserDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = User
    template_name = 'accounts/admins/user_delete.html'
    success_url = reverse_lazy('user_list')

class StoryListView(SuperAdminSidebarContextMixin, ListView):
    model = Story
    template_name = "accounts/admins/story_list.html"
    context_object_name = "stories"

class StoryCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Story
    form_class = StoryForm
    template_name = "accounts/admins/story_add.html"
    success_url = reverse_lazy("story_list")

class StoryDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Story
    template_name = 'accounts/admins/story_delete.html'
    success_url = reverse_lazy('story_list')

class PosterListView(SuperAdminSidebarContextMixin, ListView):
    model = Poster
    template_name = "accounts/admins/poster_list.html"
    context_object_name = "posters"

class PosterCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Poster
    form_class = PosterForm
    template_name = "accounts/admins/poster_add.html"
    success_url = reverse_lazy("poster_list")

class PosterDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Poster
    template_name = 'accounts/admins/poster_delete.html'
    success_url = reverse_lazy('poster_list')

class CommentListView(SuperAdminSidebarContextMixin, ListView):
    model = Comment
    template_name = "accounts/admins/comment_list.html"
    context_object_name = "comments"

class CommentCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "accounts/admins/comment_add.html"
    success_url = reverse_lazy("comment_list")

class CommentDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Comment
    template_name = 'accounts/admins/comment_delete.html'
    success_url = reverse_lazy('comment_list')

class FAQListView(SuperAdminSidebarContextMixin, ListView):
    model = FAQ
    template_name = "accounts/admins/faq_list.html"
    context_object_name = "faqs"

class FAQCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = FAQ
    form_class = FAQForm
    template_name = "accounts/admins/faq_add.html"
    success_url = reverse_lazy("faq_list")

class FAQDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = FAQ
    template_name = 'accounts/admins/faq_delete.html'
    success_url = reverse_lazy('faq_list')

class AchievementListView(SuperAdminSidebarContextMixin, ListView):
    model = Achievement
    template_name = "accounts/admins/achievement_list.html"
    context_object_name = "achievements"

class AchievementCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = "accounts/admins/achievement_add.html"
    success_url = reverse_lazy("achievement_list")

class AchievementUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = "accounts/admins/achievement_edit.html"
    success_url = reverse_lazy("achievement_list")

class AchievementDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Achievement
    template_name = 'accounts/admins/achievement_delete.html'
    success_url = reverse_lazy('achievement_list')

class LiveEventListView(SuperAdminSidebarContextMixin, ListView):
    model = LiveEvent
    template_name = "accounts/admins/live_event_list.html"
    context_object_name = "live_events"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        live_events = LiveEvent.objects.all()

        for live_event in live_events:
            live_event.start_datetime_shamsi = (
                jdatetime.date.fromgregorian(
                    date=live_event.start_datetime.date()
                ).strftime("%Y/%m/%d")
                if live_event.start_datetime
                else ""
            )

            live_event.end_datetime_shamsi = (
                jdatetime.date.fromgregorian(
                    date=live_event.end_datetime.date()
                ).strftime("%Y/%m/%d")
                if live_event.end_datetime
                else ""
            )
        
        context["live_events"] = live_events
        return context

class LiveEventCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = LiveEvent
    form_class = LiveEventForm
    template_name = "accounts/admins/live_event_add.html"
    success_url = reverse_lazy("live_event_list")

class LiveEventUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = LiveEvent
    form_class = LiveEventForm
    template_name = "accounts/admins/live_event_edit.html"
    success_url = reverse_lazy("live_event_list")

class LiveEventDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = LiveEvent
    template_name = 'accounts/admins/live_event_delete.html'
    success_url = reverse_lazy('live_event_list')

class PackageListView(SuperAdminSidebarContextMixin, ListView):
    model = Package
    template_name = "accounts/admins/package_list.html"
    context_object_name = "packages"

class PackageCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Package
    form_class = PackageForm
    template_name = "accounts/admins/package_add.html"
    success_url = reverse_lazy("package_list")

class PackageUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = Package
    form_class = PackageForm
    template_name = "accounts/admins/package_edit.html"
    success_url = reverse_lazy("package_list")

class PackageDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Package
    template_name = 'accounts/admins/package_delete.html'
    success_url = reverse_lazy('package_list')

class PlansIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = PlansIntroduction
    form_class = PlansIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class PlansIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = PlansIntroduction
    form_class = PlansIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class DataIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = DataIntroduction
    form_class = DataIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class DataIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = DataIntroduction
    form_class = DataIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class CounselingIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = CounselingIntroduction
    form_class = CounselingIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class CounselingIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = CounselingIntroduction
    form_class = CounselingIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class EstimationIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = EstimationIntroduction
    form_class = EstimationIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class EstimationIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = EstimationIntroduction
    form_class = EstimationIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class ChoiceIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = ChoiceIntroduction
    form_class = ChoiceIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class ChoiceIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = ChoiceIntroduction
    form_class = ChoiceIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class LiveIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = LiveIntroduction
    form_class = LiveIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class LiveIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = LiveIntroduction
    form_class = LiveIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class AboutUsIntroductionCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = AboutUsIntroduction
    form_class = AboutUsIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class AboutUsIntroductionUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = AboutUsIntroduction
    form_class = AboutUsIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class AllPaymentListView(SuperAdminSidebarContextMixin, ListView):
    model = Payment
    template_name = "accounts/admins/payment_list.html"
    context_object_name = "payments"

class MediaListView(SuperAdminSidebarContextMixin, ListView):
    model = Media
    template_name = "accounts/admins/media_list.html"
    context_object_name = "medias"

class MediaCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Media
    form_class = MediaForm
    template_name = "accounts/admins/media_add.html"
    success_url = reverse_lazy("media_list")

class MediaUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = Media
    form_class = MediaForm
    template_name = "accounts/admins/media_edit.html"
    success_url = reverse_lazy("media_list")

class MediaDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Media
    template_name = 'accounts/admins/media_delete.html'
    success_url = reverse_lazy('media_list')

class RankBankListView(SuperAdminSidebarContextMixin, ListView):
    model = RankBank
    template_name = "accounts/admins/rank_bank_list.html"
    context_object_name = "rank_banks"

class RankBankCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = RankBank
    form_class = RankBankForm
    template_name = "accounts/admins/rank_bank_add.html"
    success_url = reverse_lazy("rank_bank_list")

class RankBankUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = RankBank
    form_class = RankBankForm
    template_name = "accounts/admins/rank_bank_edit.html"
    success_url = reverse_lazy("rank_bank_list")

class RankBankDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = RankBank
    template_name = 'accounts/admins/rank_bank_delete.html'
    success_url = reverse_lazy('rank_bank_list')

class RuleListView(SuperAdminSidebarContextMixin, ListView):
    model = Rule
    template_name = "accounts/admins/rule_list.html"
    context_object_name = "rules"

class RuleCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Rule
    form_class = RuleForm
    template_name = "accounts/admins/rule_add.html"
    success_url = reverse_lazy("rule_list")

class RuleUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = Rule
    form_class = RuleForm
    template_name = "accounts/admins/rule_edit.html"
    success_url = reverse_lazy("rule_list")

class RuleDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = Rule
    template_name = 'accounts/admins/rule_delete.html'
    success_url = reverse_lazy('rule_list')

class StaticMessageListView(SuperAdminSidebarContextMixin, ListView):
    model = StaticMessage
    template_name = "accounts/admins/static_message_list.html"
    context_object_name = "static_messages"

class StaticMessageCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = StaticMessage
    form_class = StaticMessageForm
    template_name = "accounts/admins/static_message_add.html"
    success_url = reverse_lazy("static_message_list")

class StaticMessageUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = StaticMessage
    form_class = StaticMessageForm
    template_name = "accounts/admins/static_message_edit.html"
    success_url = reverse_lazy("static_message_list")

class StaticMessageDeleteView(SuperAdminSidebarContextMixin, DeleteView):
    model = StaticMessage
    template_name = 'accounts/admins/static_message_delete.html'
    success_url = reverse_lazy('static_message_list')

class ConsultantListView(SuperAdminSidebarContextMixin, ListView):
    model = Consultant
    template_name = "accounts/admins/consultant_list.html"
    context_object_name = "consultants"

class AdminConsultantCreateView(SuperAdminSidebarContextMixin, CreateView):
    model = Consultant
    form_class = CreateConsultantForm
    template_name = "accounts/admins/consultant_add.html"
    success_url = reverse_lazy("consultant_list")

class AdminConsultantUpdateView(SuperAdminSidebarContextMixin, UpdateView):
    model = Consultant
    form_class = ConsultantForm
    template_name = "accounts/admins/consultant_edit.html"
    success_url = reverse_lazy("consultant_list")

# endregion

# region consultant

def consultant_dashboard(request):
    return render(request, "accounts/consultants/dashboard.html")

class ConsultantCreateView(CreateView):
    model = Consultant
    form_class = ConsultantForm
    template_name = "accounts/consultants/consultant_add.html"
    success_url = reverse_lazy("consultant_dashboard")

    def form_valid(self, form):
        form.instance.consultant = self.request.user.user_consultant
        return super().form_valid(form)
    
class ConsultantUpdateView(UpdateView):
    model = Consultant
    form_class = ConsultantForm
    template_name = "accounts/consultants/consultant_edit.html"
    success_url = reverse_lazy("consultant_dashboard")

class ConsultantScheduleListView(ListView):
    model = ConsultantSchedule
    template_name = "accounts/consultants/schedule_list.html"
    context_object_name = "schedules"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedules = ConsultantSchedule.objects.filter(consultant=self.request.user.user_consultant)

        for schedule in schedules:
            consultation = Consultation.objects.filter(schedule=schedule)
            schedule.request = None

            if schedule:
                schedule.date_shamsi = jdatetime.date.fromgregorian(
                    date=schedule.date
                ).strftime('%Y/%m/%d')

                if consultation:
                    schedule.request = consultation.request
        
        context["schedules"] = schedules
        return context

class ConsultantScheduleCreateView(CreateView):
    model = ConsultantSchedule
    form_class = ConsultantScheduleForm
    template_name = "accounts/consultants/schedule_add.html"
    success_url = reverse_lazy("schedule_list")

    def form_valid(self, form):
        form.instance.consultant = self.request.user.user_consultant
        return super().form_valid(form)

class ConsultantScheduleDeleteView(DeleteView):
    model = ConsultantSchedule
    template_name = 'accounts/consultants/schedule_delete.html'
    success_url = reverse_lazy('schedule_list')

class MyStudentListView(ListView):
    model = Student
    template_name = 'accounts/consultants/my_student_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            student_packege_requests__paid=True,
            student_packege_requests__request_consultation__schedule__consultant=self.request.user.user_consultant
        ).distinct()
        return queryset

# endregion

# region student

def student_dashboard(request):
    return render(request, "accounts/students/dashboard.html")

class PaymentListView(ListView):
    model = Payment
    template_name = "accounts/students/payment_list.html"
    context_object_name = "payments"

    def get_queryset(self):
        queryset = super().get_queryset().filter(order__student=self.request.user.user_student)

        return queryset

def rank_form(request):
    student = request.user.user_student    
    
    try:
        rank = student.student_rank
    except Rank.DoesNotExist:
        rank = None

    if request.method == "POST":
        form = RankForm(request.POST, request.FILES, instance=rank)

        if form.is_valid():
            rank_obj = form.save(commit=False)
            rank_obj.student = student
            rank_obj.save()

            return redirect("plans")
    else:
        form = RankForm(instance=rank)

    return render(
        request,
        "accounts/students/rank_form.html",
        {
            "form": form,
        },
    )

def personality60(request):
    student = request.user.user_student

    # آیا خدمت تحلیل شخصیت را خریده؟
    has_service = ServiceToStudent.objects.filter(
        student=student,
        service="3"   # تحلیل شخصیت
    ).exists()

    if not has_service:
        messages.error(request, "شما دسترسی به این آزمون را ندارید.")
        return redirect("plans")

    # آیا قبلاً آزمون را تکمیل کرده؟
    personality = Personality60.objects.filter(student=student).first()
    form_a = AB.objects.filter(student=student).first()

    if personality and not student.a_completed:
        ab, created = AB.objects.get_or_create(student=student)

        if request.method == "POST":
            form = AForm(request.POST, instance=ab)

            if form.is_valid():
                form = form.save(commit=False)
                form.student = student
                form.save()

                student.a_completed = True
                student.save(update_fields=["a_completed"])

                return redirect("personality60")
        else:
            form = AForm(instance=ab)

        return render(
            request,
            "accounts/students/a_form.html",
            {
                "form": form,
            },
        )

    if personality and student.a_completed:
        answers = {
            f"q{i}": getattr(personality, f"q{i}")
            for i in range(1, 61)
        }

        calculate_item_scores_result = calculate_item_scores(answers)
        detect_personality_type_result = detect_personality_type(calculate_item_scores_result)
        personal_modifier_result = personal_modifier(form_a)
        calculate_specialty_scores_result = calculate_specialty_scores(calculate_item_scores_result)
        apply_personal_modifier_result = apply_personal_modifier(calculate_specialty_scores_result, personal_modifier_result)
        categorize_specialties_result = categorize_specialties(apply_personal_modifier_result)

        return render(
            request,
            "accounts/students/personality60_result.html",
            {
                "calculate_item_scores_result": calculate_item_scores_result,
                "detect_personality_type_result": detect_personality_type_result,
                "categorize_specialties_result": categorize_specialties_result,
                "personality": personality,
            },
        )

    # هنوز پر نکرده
    if request.method == "POST":
        form = Personality60Form(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = student
            obj.save()

            return redirect("personality60")

    else:
        form = Personality60Form()

    return render(
        request,
        "accounts/students/personality60_form.html",
        {
            "form": form,
        },
    )

def validity(request):
    student = request.user.user_student

    has_service = ServiceToStudent.objects.filter(
        student=student,
        service="4"
    ).exists()

    if not has_service:
        messages.error(request, "شما دسترسی به این آزمون را ندارید.")
        return redirect("plans")
    
    try:
        rank = student.student_rank
    except Rank.DoesNotExist:
        rank = None

    if rank:
        calculate_class = AdmissionPredictor(VALIDITY, UNIVERSITY, FIELD, UNDERUTILIZED)
        calculate_result = calculate_class.predict(rank)

        return render(
            request,
            "accounts/students/validity_result.html",
            {
                "calculate_result": calculate_result,
            },
        )
    else:
        if request.method == "POST":
            form = RankForm(request.POST, request.FILES, instance=rank)

            if form.is_valid():
                rank = form.save(commit=False)
                rank.student = student
                rank.save()

                return redirect("validity")
        else:
            form = RankForm(instance=rank)

        return render(
            request,
            "accounts/students/rank_form.html",
            {
                "form": form,
            },
        )
    
    # if not student.b_completed:
    #     ab, created = AB.objects.get_or_create(student=student)

    #     if request.method == "POST":
    #         form = BForm(request.POST, instance=ab)

    #         if form.is_valid():
    #             form.save()

    #             student.b_completed = True
    #             student.save(update_fields=["b_completed"])

    #             student.a_completed = True
    #             student.save(update_fields=["a_completed"])

    #             return redirect("validity")
    #     else:
    #         form = BForm(instance=ab)

    #     return render(
    #         request,
    #         "accounts/students/b_form.html",
    #         {
    #             "form": form,
    #         },
    #     )

# endregion
import re
import jdatetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
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
from .mixins import SuperAdminSidebarContextMixin, RoleRequiredMixin

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

def mobile_login(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile", "").strip()

        if not mobile:
            messages.error(request, "شماره موبایل را وارد کنید.")
            return redirect("login")

        is_valid, mobile = validate_mobile(mobile)
        
        if not is_valid:
            messages.error(request, "شماره موبایل معتبر نیست.")
            return redirect("login")

        request.session["auth_mobile"] = mobile

        try:
            user = User.objects.get(username=mobile)
        except User.DoesNotExist:
            user = None

        if user:

            if user.is_suspended:
                messages.error(request, "حساب کاربری شما تعلیق شده است.")
                request.session.pop("auth_mobile", None)
                return redirect("login")

            return redirect("password-login")

        last_otp = OTP.objects.filter(
            mobile=mobile,
            is_used=False
        ).last()

        if last_otp and last_otp.is_valid():
            messages.warning(
                request,
                "کد قبلاً ارسال شده است. لطفاً همان کد را وارد کنید."
            )
            return redirect("verify-otp")

        code = generate_code()

        OTP.objects.create(
            mobile=mobile,
            code=code
        )

        send_sms(mobile, code)

        return redirect("verify-otp")

    return render(request, "accounts/mobile_login.html")

def password_login(request):

    mobile = request.session.get("auth_mobile")

    if not mobile:
        return redirect("login")

    user = User.objects.filter(mobile=mobile).first()

    if user is None:
        return redirect("login")

    if request.method == "POST":

        password = request.POST.get("password", "").strip()

        user = authenticate(
            username=mobile,
            password=password
        )

        if user is None:
            messages.error(request, "رمز عبور صحیح نیست.")
            return redirect("password-login")

        login(request, user)

        request.session.pop("auth_mobile", None)

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
        "accounts/password_login.html",
        {
            "mobile": mobile
        }
    )

def verify_otp(request):

    mobile = request.session.get("auth_mobile")

    if not mobile:
        return redirect("login")

    otp = OTP.objects.filter(
        mobile=mobile,
        is_used=False
    ).last()

    if otp is None:
        messages.error(request, "ابتدا درخواست کد تأیید بدهید.")
        return redirect("login")

    if request.method == "POST":

        code = request.POST.get("code", "").strip()

        if otp.code != code:
            messages.error(request, "کد وارد شده صحیح نیست.")
            return redirect("verify-otp")

        if not otp.is_valid():
            messages.error(request, "زمان اعتبار کد به پایان رسیده است.")
            return redirect("login")

        otp.is_used = True
        otp.save()

        user = User.objects.create(
            username=mobile,
            mobile=mobile,
            password=make_password(code),
            role="student"
        )

        user = authenticate(
            username=mobile,
            password=code
        )

        login(request, user)

        request.session.pop("auth_mobile", None)

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
        "accounts/verify_otp.html",
        {
            "otp": otp,
            "mobile": mobile,
        }
    )

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

@login_required
def admin_dashboard(request):
    aside = aside_super_admin_context()
    return render(request, "accounts/admins/dashboard.html", aside)

class UserListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = User
    template_name = "accounts/admins/user_list.html"
    context_object_name = "users"

class UserCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = User
    form_class = UserCreationForm
    template_name = "accounts/admins/user_add.html"
    success_url = reverse_lazy("user_list")

class UserUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = User
    form_class = UserForm
    template_name = "accounts/admins/user_edit.html"
    success_url = reverse_lazy("user_list")

class UserDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = User
    template_name = 'accounts/admins/user_delete.html'
    success_url = reverse_lazy('user_list')

class StoryListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Story
    template_name = "accounts/admins/story_list.html"
    context_object_name = "stories"

class StoryCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Story
    form_class = StoryForm
    template_name = "accounts/admins/story_add.html"
    success_url = reverse_lazy("story_list")

class StoryDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Story
    template_name = 'accounts/admins/story_delete.html'
    success_url = reverse_lazy('story_list')

class PosterListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Poster
    template_name = "accounts/admins/poster_list.html"
    context_object_name = "posters"

class PosterCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Poster
    form_class = PosterForm
    template_name = "accounts/admins/poster_add.html"
    success_url = reverse_lazy("poster_list")

class PosterDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Poster
    template_name = 'accounts/admins/poster_delete.html'
    success_url = reverse_lazy('poster_list')

class CommentListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Comment
    template_name = "accounts/admins/comment_list.html"
    context_object_name = "comments"

class CommentCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Comment
    form_class = CommentForm
    template_name = "accounts/admins/comment_add.html"
    success_url = reverse_lazy("comment_list")

class CommentDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Comment
    template_name = 'accounts/admins/comment_delete.html'
    success_url = reverse_lazy('comment_list')

class FAQListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = FAQ
    template_name = "accounts/admins/faq_list.html"
    context_object_name = "faqs"

class FAQCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = FAQ
    form_class = FAQForm
    template_name = "accounts/admins/faq_add.html"
    success_url = reverse_lazy("faq_list")

class FAQDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = FAQ
    template_name = 'accounts/admins/faq_delete.html'
    success_url = reverse_lazy('faq_list')

class AchievementListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Achievement
    template_name = "accounts/admins/achievement_list.html"
    context_object_name = "achievements"

class AchievementCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Achievement
    form_class = AchievementForm
    template_name = "accounts/admins/achievement_add.html"
    success_url = reverse_lazy("achievement_list")

class AchievementUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = Achievement
    form_class = AchievementForm
    template_name = "accounts/admins/achievement_edit.html"
    success_url = reverse_lazy("achievement_list")

class AchievementDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Achievement
    template_name = 'accounts/admins/achievement_delete.html'
    success_url = reverse_lazy('achievement_list')

class LiveEventListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
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

class LiveEventCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = LiveEvent
    form_class = LiveEventForm
    template_name = "accounts/admins/live_event_add.html"
    success_url = reverse_lazy("live_event_list")

class LiveEventUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = LiveEvent
    form_class = LiveEventForm
    template_name = "accounts/admins/live_event_edit.html"
    success_url = reverse_lazy("live_event_list")

class LiveEventDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = LiveEvent
    template_name = 'accounts/admins/live_event_delete.html'
    success_url = reverse_lazy('live_event_list')

class PackageListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Package
    template_name = "accounts/admins/package_list.html"
    context_object_name = "packages"

class PackageCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Package
    form_class = PackageForm
    template_name = "accounts/admins/package_add.html"
    success_url = reverse_lazy("package_list")

class PackageUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = Package
    form_class = PackageForm
    template_name = "accounts/admins/package_edit.html"
    success_url = reverse_lazy("package_list")

class PackageDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Package
    template_name = 'accounts/admins/package_delete.html'
    success_url = reverse_lazy('package_list')

class PlansIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = PlansIntroduction
    form_class = PlansIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class PlansIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = PlansIntroduction
    form_class = PlansIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class DataIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = DataIntroduction
    form_class = DataIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class DataIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = DataIntroduction
    form_class = DataIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class CounselingIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = CounselingIntroduction
    form_class = CounselingIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class CounselingIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = CounselingIntroduction
    form_class = CounselingIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class EstimationIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = EstimationIntroduction
    form_class = EstimationIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class EstimationIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = EstimationIntroduction
    form_class = EstimationIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class ChoiceIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = ChoiceIntroduction
    form_class = ChoiceIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class ChoiceIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = ChoiceIntroduction
    form_class = ChoiceIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class LiveIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = LiveIntroduction
    form_class = LiveIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class LiveIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = LiveIntroduction
    form_class = LiveIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class AboutUsIntroductionCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = AboutUsIntroduction
    form_class = AboutUsIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class AboutUsIntroductionUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = AboutUsIntroduction
    form_class = AboutUsIntroductionForm
    template_name = "accounts/intro/form.html"
    success_url = reverse_lazy("admin_dashboard")

class AllPaymentListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Payment
    template_name = "accounts/admins/payment_list.html"
    context_object_name = "payments"

class MediaListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Media
    template_name = "accounts/admins/media_list.html"
    context_object_name = "medias"

class MediaCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Media
    form_class = MediaForm
    template_name = "accounts/admins/media_add.html"
    success_url = reverse_lazy("media_list")

class MediaUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = Media
    form_class = MediaForm
    template_name = "accounts/admins/media_edit.html"
    success_url = reverse_lazy("media_list")

class MediaDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Media
    template_name = 'accounts/admins/media_delete.html'
    success_url = reverse_lazy('media_list')

class RankBankListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = RankBank
    template_name = "accounts/admins/rank_bank_list.html"
    context_object_name = "rank_banks"

class RankBankCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = RankBank
    form_class = RankBankForm
    template_name = "accounts/admins/rank_bank_add.html"
    success_url = reverse_lazy("rank_bank_list")

class RankBankUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = RankBank
    form_class = RankBankForm
    template_name = "accounts/admins/rank_bank_edit.html"
    success_url = reverse_lazy("rank_bank_list")

class RankBankDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = RankBank
    template_name = 'accounts/admins/rank_bank_delete.html'
    success_url = reverse_lazy('rank_bank_list')

class RuleListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Rule
    template_name = "accounts/admins/rule_list.html"
    context_object_name = "rules"

class RuleCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Rule
    form_class = RuleForm
    template_name = "accounts/admins/rule_add.html"
    success_url = reverse_lazy("rule_list")

class RuleUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = Rule
    form_class = RuleForm
    template_name = "accounts/admins/rule_edit.html"
    success_url = reverse_lazy("rule_list")

class RuleDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = Rule
    template_name = 'accounts/admins/rule_delete.html'
    success_url = reverse_lazy('rule_list')

class StaticMessageListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = StaticMessage
    template_name = "accounts/admins/static_message_list.html"
    context_object_name = "static_messages"

class StaticMessageCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = StaticMessage
    form_class = StaticMessageForm
    template_name = "accounts/admins/static_message_add.html"
    success_url = reverse_lazy("static_message_list")

class StaticMessageUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = StaticMessage
    form_class = StaticMessageForm
    template_name = "accounts/admins/static_message_edit.html"
    success_url = reverse_lazy("static_message_list")

class StaticMessageDeleteView(RoleRequiredMixin, SuperAdminSidebarContextMixin, DeleteView):
    allowed_roles = ["super_admin"]
    model = StaticMessage
    template_name = 'accounts/admins/static_message_delete.html'
    success_url = reverse_lazy('static_message_list')

class ConsultantListView(RoleRequiredMixin, SuperAdminSidebarContextMixin, ListView):
    allowed_roles = ["super_admin"]
    model = Consultant
    template_name = "accounts/admins/consultant_list.html"
    context_object_name = "consultants"

class AdminConsultantCreateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, CreateView):
    allowed_roles = ["super_admin"]
    model = Consultant
    form_class = CreateConsultantForm
    template_name = "accounts/admins/consultant_add.html"
    success_url = reverse_lazy("consultant_list")

class AdminConsultantUpdateView(RoleRequiredMixin, SuperAdminSidebarContextMixin, UpdateView):
    allowed_roles = ["super_admin"]
    model = Consultant
    form_class = ConsultantForm
    template_name = "accounts/admins/consultant_edit.html"
    success_url = reverse_lazy("consultant_list")

class AdminConsultantScheduleListView(ListView):
    model = ConsultantSchedule
    template_name = "accounts/admins/schedule_list.html"
    context_object_name = "schedules"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        schedules = ConsultantSchedule.objects.all()

        for schedule in schedules:

            consultation = Consultation.objects.filter(
                schedule=schedule
            ).select_related("service__student__user").first()

            schedule.request = consultation

            schedule.date_shamsi = jdatetime.date.fromgregorian(
                date=schedule.date
            ).strftime("%Y/%m/%d")

        context["schedules"] = schedules
        return context

class AdminConsultantScheduleDeleteView(DeleteView):
    model = ConsultantSchedule
    template_name = 'accounts/admins/schedule_delete.html'
    success_url = reverse_lazy('schedule_list')

def show_student(request, id):

    user = get_object_or_404(User, id=id)

    context = {
        "user": user,
    }

    student = getattr(user, "user_student", None)

    if student:

        # ---------- Rank ----------
        if hasattr(student, "student_rank"):

            rank_fields = []

            for field in student.student_rank._meta.fields:

                if field.name in ["id", "student"]:
                    continue

                value = getattr(student.student_rank, field.name)

                if hasattr(field, "choices") and field.choices:
                    value = getattr(
                        student.student_rank,
                        f"get_{field.name}_display"
                    )()

                rank_fields.append({
                    "label": field.verbose_name,
                    "value": value,
                })

            context["rank_fields"] = rank_fields

        # ---------- AB ----------
        if hasattr(student, "student_AB"):

            ab_fields = []

            for field in student.student_AB._meta.fields:

                if field.name in ["id", "student"]:
                    continue

                value = getattr(student.student_AB, field.name)

                if hasattr(field, "choices") and field.choices:
                    value = getattr(
                        student.student_AB,
                        f"get_{field.name}_display"
                    )()

                ab_fields.append({
                    "label": field.verbose_name,
                    "value": value,
                })

            context["ab_fields"] = ab_fields

        # ---------- Personality ----------
        if hasattr(student, "student_personality_60"):

            personality_fields = []

            for field in student.student_personality_60._meta.fields:

                if field.name in ["id", "student"]:
                    continue

                value = getattr(student.student_personality_60, field.name)

                if hasattr(field, "choices") and field.choices:
                    value = getattr(
                        student.student_personality_60,
                        f"get_{field.name}_display"
                    )()

                personality_fields.append({
                    "label": field.verbose_name,
                    "value": value,
                })

            context["personality_fields"] = personality_fields

    return render(
        request,
        "accounts/consultants/show_my_student.html",
        context
    )

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

        schedules = ConsultantSchedule.objects.filter(
            consultant=self.request.user.user_consultant
        )

        for schedule in schedules:

            consultation = Consultation.objects.filter(
                schedule=schedule
            ).select_related("service__student__user").first()

            schedule.request = consultation

            schedule.date_shamsi = jdatetime.date.fromgregorian(
                date=schedule.date
            ).strftime("%Y/%m/%d")

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

def show_my_student(request, id):

    user = get_object_or_404(User, id=id)

    context = {
        "user": user,
    }

    student = getattr(user, "user_student", None)

    if student:

        # ---------- Rank ----------
        if hasattr(student, "student_rank"):

            rank_fields = []

            for field in student.student_rank._meta.fields:

                if field.name in ["id", "student"]:
                    continue

                value = getattr(student.student_rank, field.name)

                if hasattr(field, "choices") and field.choices:
                    value = getattr(
                        student.student_rank,
                        f"get_{field.name}_display"
                    )()

                rank_fields.append({
                    "label": field.verbose_name,
                    "value": value,
                })

            context["rank_fields"] = rank_fields

        # ---------- AB ----------
        if hasattr(student, "student_AB"):

            ab_fields = []

            for field in student.student_AB._meta.fields:

                if field.name in ["id", "student"]:
                    continue

                value = getattr(student.student_AB, field.name)

                if hasattr(field, "choices") and field.choices:
                    value = getattr(
                        student.student_AB,
                        f"get_{field.name}_display"
                    )()

                ab_fields.append({
                    "label": field.verbose_name,
                    "value": value,
                })

            context["ab_fields"] = ab_fields

        # ---------- Personality ----------
        if hasattr(student, "student_personality_60"):

            personality_fields = []

            for field in student.student_personality_60._meta.fields:

                if field.name in ["id", "student"]:
                    continue

                value = getattr(student.student_personality_60, field.name)

                if hasattr(field, "choices") and field.choices:
                    value = getattr(
                        student.student_personality_60,
                        f"get_{field.name}_display"
                    )()

                personality_fields.append({
                    "label": field.verbose_name,
                    "value": value,
                })

            context["personality_fields"] = personality_fields

    return render(
        request,
        "accounts/consultants/show_my_student.html",
        context
    )

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
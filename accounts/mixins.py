from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from pages.models import (
    PlansIntroduction, CounselingIntroduction, EstimationIntroduction,
    ChoiceIntroduction, LiveIntroduction, AboutUsIntroduction, DataIntroduction
)

class SuperAdminSidebarContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "PlansIntroductionCreated": PlansIntroduction.objects.first(),
            "CounselingIntroductionCreated": CounselingIntroduction.objects.first(),
            "EstimationIntroductionCreated": EstimationIntroduction.objects.first(),
            "ChoiceIntroductionCreated": ChoiceIntroduction.objects.first(),
            "LiveIntroductionCreated": LiveIntroduction.objects.first(),
            "AboutUsIntroductionCreated": AboutUsIntroduction.objects.first(),
            "DataIntroductionCreated": DataIntroduction.objects.first(),
        })
        return context

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return (
            self.request.user.is_authenticated and
            self.request.user.role in self.allowed_roles and
            not self.request.user.is_suspended
        )

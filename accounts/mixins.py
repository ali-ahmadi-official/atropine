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

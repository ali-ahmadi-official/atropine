import jdatetime
from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from pages.models import (
    News, Story, LiveEvent, Achievement, Survey, SurveyOption, PlansIntroduction,
    CounselingIntroduction, EstimationIntroduction, ChoiceIntroduction, LiveIntroduction,
)
from payments.models import Package
from .models import User, Consultant, ConsultantSchedule, Rank, AB, Personality60

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if not isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-control"
            else:
                widget.attrs["class"] = "form-check-input"

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "role",
            "mobile",
            "avatar",
        )

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام کاربری",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی",
            }),
            "role": forms.Select(attrs={
                "class": "form-select",
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "09xxxxxxxxx",
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }

    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "رمز عبور",
        }),
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "تکرار رمز عبور",
        }),
    )

class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "mobile", "avatar"]

class ConsultantForm(BaseModelForm):
    class Meta:
        model = Consultant
        exclude = ("user",)

class ConsultantScheduleForm(BaseModelForm):
    date = forms.CharField(
        label="تاریخ",
        required=True,
    )

    start_time = forms.TimeField(
        label="ساعت شروع",
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
            }
        ),
        required=True,
    )

    end_time = forms.TimeField(
        label="ساعت پایان",
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
            }
        ),
        required=True,
    )

    class Meta:
        model = ConsultantSchedule
        exclude = ("consultant",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["date"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "1405/04/12",
        })

        if self.instance.pk:
            self.fields["date"].initial = (
                jdatetime.date.fromgregorian(date=self.instance.date)
                .strftime("%Y/%m/%d")
            )

    def clean(self):
        cleaned_data = super().clean()

        try:
            jy, jm, jd = map(int, cleaned_data["date"].split("/"))
            cleaned_data["date"] = (
                jdatetime.date(jy, jm, jd)
                .togregorian()
            )

            if (
                cleaned_data["start_time"]
                >= cleaned_data["end_time"]
            ):
                raise forms.ValidationError(
                    "ساعت پایان باید بعد از ساعت شروع باشد."
                )

        except ValueError:
            raise forms.ValidationError("فرمت تاریخ صحیح نیست.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.date = self.cleaned_data["date"]

        if commit:
            instance.save()

        return instance

class NewsForm(BaseModelForm):
    class Meta:
        model = News
        fields = "__all__"

class StoryForm(BaseModelForm):
    class Meta:
        model = Story
        fields = "__all__"

class LiveEventForm(BaseModelForm):
    start_date = forms.CharField(
        label="تاریخ شروع",
        required=True
    )

    start_time = forms.TimeField(
        label="ساعت شروع",
        widget=forms.TimeInput(attrs={"type": "time"}),
        required=True
    )

    end_date = forms.CharField(
        label="تاریخ پایان",
        required=True
    )

    end_time = forms.TimeField(
        label="ساعت پایان",
        widget=forms.TimeInput(attrs={"type": "time"}),
        required=True
    )

    class Meta:
        model = LiveEvent
        exclude = ("start_datetime", "end_datetime")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            start = jdatetime.datetime.fromgregorian(datetime=self.instance.start_datetime)
            end = jdatetime.datetime.fromgregorian(datetime=self.instance.end_datetime)

            self.fields["start_date"].initial = start.strftime("%Y/%m/%d")
            self.fields["start_time"].initial = start.strftime("%H:%M")

            self.fields["end_date"].initial = end.strftime("%Y/%m/%d")
            self.fields["end_time"].initial = end.strftime("%H:%M")

    def clean(self):
        cleaned_data = super().clean()

        try:
            # شروع
            jy, jm, jd = map(int, cleaned_data["start_date"].split("/"))
            start_jalali = jdatetime.datetime(
                jy,
                jm,
                jd,
                cleaned_data["start_time"].hour,
                cleaned_data["start_time"].minute,
            )
            start = start_jalali.togregorian()
            start = timezone.make_aware(start, timezone.get_current_timezone())
            cleaned_data["start_datetime"] = start

            # پایان
            jy, jm, jd = map(int, cleaned_data["end_date"].split("/"))
            end_jalali = jdatetime.datetime(
                jy,
                jm,
                jd,
                cleaned_data["end_time"].hour,
                cleaned_data["end_time"].minute,
            )
            end = end_jalali.togregorian()
            end = timezone.make_aware(end, timezone.get_current_timezone())
            cleaned_data["end_datetime"] = end

            if cleaned_data["start_datetime"] >= cleaned_data["end_datetime"]:
                raise forms.ValidationError("زمان پایان باید بعد از زمان شروع باشد.")

        except Exception:
            raise forms.ValidationError("فرمت تاریخ صحیح نیست.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.start_datetime = self.cleaned_data["start_datetime"]
        instance.end_datetime = self.cleaned_data["end_datetime"]

        if commit:
            instance.save()

        return instance

class AchievementForm(BaseModelForm):
    class Meta:
        model = Achievement
        fields = "__all__"

class SurveyForm(BaseModelForm):
    class Meta:
        model = Survey
        fields = "__all__"

class SurveyOptionForm(BaseModelForm):
    class Meta:
        model = SurveyOption
        fields = "__all__"

class PlansIntroductionForm(BaseModelForm):
    class Meta:
        model = PlansIntroduction
        fields = "__all__"

class CounselingIntroductionForm(BaseModelForm):
    class Meta:
        model = CounselingIntroduction
        fields = "__all__"

class EstimationIntroductionForm(BaseModelForm):
    class Meta:
        model = EstimationIntroduction
        fields = "__all__"

class ChoiceIntroductionForm(BaseModelForm):
    class Meta:
        model = ChoiceIntroduction
        fields = "__all__"

class LiveIntroductionForm(BaseModelForm):
    class Meta:
        model = LiveIntroduction
        fields = "__all__"

class PackageForm(BaseModelForm):
    class Meta:
        model = Package
        fields = "__all__"

        widgets = {
            "service": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "total_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

class RankForm(BaseModelForm):
    class Meta:
        model = Rank
        exclude = ["student"]

class AForm(BaseModelForm):
    class Meta:
        model = AB
        fields = [
            "gender",
            "marital",
            "wife_condition",
            "child",
            "family_support",
            "interest_surgical",
            "interest_non_surgical",
            "field_preference",
            "paraclinic_preference",
            "income_importance",
            "residency_free_time_importance",
            "career_free_time_importance",
            "no_night_shift_importance",
            "private_practice_interest",
            "academic_interest",
            "immigration_interest",
            "better_activity",
            "favorite_activity",
            "guard",
        ]

        widgets = {
            "better_activity": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            ),
            "favorite_activity": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            )
        }

class BForm(BaseModelForm):
    class Meta:
        model = AB
        exclude = ["student"]

        widgets = {
            "better_activity": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            ),
            "favorite_activity": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            ),
            "quota": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            ),
            "commitment": forms.SelectMultiple(
                attrs={
                    "class": "form-select select2",
                }
            )
        }

class Personality60Form(BaseModelForm):
    class Meta:
        model = Personality60
        exclude = ["student"]

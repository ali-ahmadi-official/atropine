from django import forms
from accounts.models import Rank, AB, Personality60

class CompleteProfileForm(forms.Form):
    first_name = forms.CharField(
        label="نام",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خود را وارد کنید",
            }
        ),
    )

    last_name = forms.CharField(
        label="نام خانوادگی",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی خود را وارد کنید",
            }
        ),
    )

    mobile = forms.CharField(
        label="شماره موبایل",
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "09xxxxxxxxx",
                "dir": "ltr",
            }
        ),
    )

class RankForm(forms.ModelForm):

    class Meta:
        model = Rank
        exclude = ("student",)

        widgets = {
            "report_image": forms.FileInput(attrs={
                "class": "form-control"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    "class": "form-control"
                })

class ABForm(forms.ModelForm):

    class Meta:
        model = AB
        exclude = ("student",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.CheckboxInput):
                continue

            field.widget.attrs.update({
                "class": "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            })

class Personality60Form(forms.ModelForm):

    class Meta:
        model = Personality60
        exclude = ("student",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            })

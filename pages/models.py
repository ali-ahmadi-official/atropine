from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .validators import validate_video

class News(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    image = models.ImageField(
        upload_to="news/",
        verbose_name="تصویر"
    )

    content = models.TextField(
        verbose_name="متن"
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name="نمایش عمومی"
    )

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "خبرها"

class Story(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    cover = models.ImageField(
        upload_to="stories/cover/",
        verbose_name="کاور"
    )

    content = models.FileField(
        upload_to="stories/content/",
        verbose_name="محتوا استوری"
    )

    class Meta:
        verbose_name = "استوری"
        verbose_name_plural = "استوری ها"

class LiveEvent(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان لایو"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    cover = models.ImageField(
        upload_to="live_events/",
        verbose_name="کاور"
    )

    start_datetime = models.DateTimeField(
        verbose_name="زمان شروع"
    )

    end_datetime = models.DateTimeField(
        verbose_name="زمان پایان"
    )

    stream_url = models.URLField(
        verbose_name="لینک پخش"
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name="نمایش عمومی"
    )

    class Meta:
        verbose_name = "لایو"
        verbose_name_plural = "لایوها"

class Achievement(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name="نام و نام خانوادگی"
    )

    rank = models.CharField(
        max_length=255,
        verbose_name="مقام یا رتبه"
    )

    cover = models.ImageField(
        upload_to="achievements/",
        verbose_name="کاور"
    )

    class Meta:
        verbose_name = "افتخار"
        verbose_name_plural = "افتخارات"

# class Notification(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="کاربر"
#     )

#     title = models.CharField(
#         max_length=255,
#         verbose_name="عنوان"
#     )

#     message = models.TextField(
#         verbose_name="متن پیام"
#     )

#     is_read = models.BooleanField(
#         default=False,
#         verbose_name="خوانده شده"
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="تاریخ"
#     )

#     class Meta:
#         verbose_name = "اعلان"
#         verbose_name_plural = "اعلان ها"

class Survey(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان نظرسنجی"
    )

    class Meta:
        verbose_name = "نظرسنجی"
        verbose_name_plural = "نظرسنجی ها"


class SurveyOption(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        verbose_name="نظرسنجی"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="گزینه"
    )

    class Meta:
        verbose_name = "گزینه نظرسنجی"
        verbose_name_plural = "گزینه های نظرسنجی"

class PlansIntroduction(models.Model):
    video = models.FileField(
        upload_to="introductions/counseling/",
        validators=[validate_video],
        verbose_name="ویدئو معرفی"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "معرفی خدمت"
        verbose_name_plural = "معرفی های خدمت"

class CounselingIntroduction(models.Model):
    video = models.FileField(
        upload_to="introductions/counseling/",
        validators=[validate_video],
        verbose_name="ویدئو معرفی"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "معرفی مشاوره"
        verbose_name_plural = "معرفی های مشاوره"

class EstimationIntroduction(models.Model):
    video = models.FileField(
        upload_to="introductions/counseling/",
        validators=[validate_video],
        verbose_name="ویدئو معرفی"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "معرفی تخمین قبولی"
        verbose_name_plural = "معرفی های تخمین قبولی"

class ChoiceIntroduction(models.Model):
    video = models.FileField(
        upload_to="introductions/counseling/",
        validators=[validate_video],
        verbose_name="ویدئو معرفی"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "معرفی انتخاب رشته"
        verbose_name_plural = "معرفی های انتخاب رشته"

class LiveIntroduction(models.Model):
    video = models.FileField(
        upload_to="introductions/counseling/",
        validators=[validate_video],
        verbose_name="ویدئو معرفی"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "معرفی وبینار"
        verbose_name_plural = "معرفی های وبینار"

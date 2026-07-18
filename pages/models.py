from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from multiselectfield import MultiSelectField
from .validators import validate_video

SHOW_IN_CHOICES = (
    ("main", "صفحه خانه"),
    ("compass", "صفحه قطب نمای آتروپین"),
    ("choice", "صفحه جلسات فردی انتخاب رشته"),
    ("archives", "صفحه آرشیو لایو های سال های قبل"),
)

MEDIA_TYPE_CHOICES = (
    ("video", "ویدئوهای معرفی اختصاصی رشته ها"),
    ("voice", "ویس های بررسی رشته شهرها"),
    ("else_video", "سایر ویدئوها"),
    ("else_voice", "سایر ویس ها"),
)

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

    show_in = MultiSelectField(
        max_length=100,
        choices=SHOW_IN_CHOICES,
        verbose_name="نمایش در صفحات"
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

    show_in = MultiSelectField(
        max_length=100,
        choices=SHOW_IN_CHOICES,
        verbose_name="نمایش در صفحات"
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

class DataIntroduction(models.Model):
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
        verbose_name = "معرفی پایگاه داده"
        verbose_name_plural = "معرفی های پایگاه داده"

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

class AboutUsIntroduction(models.Model):
    video = models.FileField(
        upload_to="introductions/about_us/",
        validators=[validate_video],
        verbose_name="ویدئو معرفی"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "معرفی ما"
        verbose_name_plural = "معرفی های ما"

class Poster(models.Model):
    cover = models.ImageField(
        upload_to="posters/",
        verbose_name="پوستر"
    )

    show_in = MultiSelectField(
        max_length=100,
        choices=SHOW_IN_CHOICES,
        verbose_name="نمایش در صفحات"
    )

    stream_url = models.URLField(
        verbose_name="لینک پخش",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "پوستر"
        verbose_name_plural = "پوستر ها"

class Comment(models.Model):
    cover = models.ImageField(
        upload_to="comments/",
        verbose_name="پروفایل"
    )

    content = models.CharField(
        max_length=300,
        verbose_name="نظر"
    )

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

class FAQ(models.Model):
    question = models.CharField(
        max_length=500,
        verbose_name="سوال"
    )

    answer = models.CharField(
        max_length=500,
        verbose_name="پاسخ"
    )

    class Meta:
        verbose_name = "پرسش و پاسخ"
        verbose_name_plural = "پرسش و پاسخ ها"

class Media(models.Model):
    content = models.FileField(
        upload_to="media_content/",
        verbose_name="محتوا"
    )

    cover = models.ImageField(
        upload_to="media_cover/",
        verbose_name="کاور",
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    description = models.TextField(
        verbose_name="توضیحات"
    )

    media_type = models.CharField(
        max_length=100,
        choices=MEDIA_TYPE_CHOICES,
        verbose_name="نوع مدیا"
    )

    is_free = models.BooleanField(
        default=False,
        verbose_name="رایگان"
    )

    class Meta:
        verbose_name = "مدیا"
        verbose_name_plural = "مدیا ها"

class RankBank(models.Model):
    QUOTA_CHOICES = (
        ("1", "آزاد"),
        ("2", "محروم"),
        ("3", "ایثارگران ۵٪"),
        ("4", "ایثارگران ۲۵٪"),
        ("5", "سایر"),
    )

    rank = models.PositiveIntegerField(
        verbose_name="رتبه"
    )

    quota = models.CharField(
        max_length=1,
        choices=QUOTA_CHOICES,
        verbose_name="سهمیه"
    )

    field = models.CharField(
        max_length=200,
        verbose_name="رشته قبولی"
    )

    description = models.CharField(
        max_length=500,
        verbose_name="توضیحات",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "رتبه قبولی"
        verbose_name_plural = "رتبه قبولی ها"

class Rule(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان"
    )

    description = models.TextField(
        verbose_name="توضیحات"
    )

    image = models.ImageField(
        upload_to="rules/",
        verbose_name="تصویر",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "قانون"
        verbose_name_plural = "قوانین"

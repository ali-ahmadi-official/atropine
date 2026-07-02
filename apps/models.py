from django.db import models
from accounts.models import User

class Course(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان دوره"
    )

    description = models.TextField(
        verbose_name="توضیحات"
    )

    image = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True,
        verbose_name="تصویر"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="هزینه"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره ها"

class CourseConsultant(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="دوره"
    )

    consultant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="مشاور"
    )

    class Meta:
        verbose_name = "مشاور دوره"
        verbose_name_plural = "مشاوران دوره"

class StudyPlan(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="داوطلب"
    )

    consultant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name="مشاور"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان برنامه"
    )

    week_start = models.DateField(
        verbose_name="شروع هفته"
    )

    class Meta:
        verbose_name = "برنامه مطالعاتی"
        verbose_name_plural = "برنامه های مطالعاتی"

class StudyTask(models.Model):
    STATUS_CHOICES = (
        ("pending", "انجام نشده"),
        ("done", "انجام شده"),
        ("failed", "انجام نشده توسط داوطلب"),
    )

    plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        verbose_name="برنامه"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان فعالیت"
    )

    study_date = models.DateField(
        verbose_name="تاریخ"
    )

    estimated_minutes = models.PositiveIntegerField(
        verbose_name="زمان پیشنهادی"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت"
    )

    class Meta:
        verbose_name = "باکس برنامه"
        verbose_name_plural = "باکس های برنامه"

class ContentCategory(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="دسته والد"
    )

    class Meta:
        verbose_name = "دسته بندی محتوا"
        verbose_name_plural = "دسته بندی های محتوا"

class Content(models.Model):
    CONTENT_TYPES = (
        ("video", "ویدئو"),
        ("audio", "صوت"),
        ("pdf", "فایل PDF"),
        ("article", "مقاله"),
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    category = models.ForeignKey(
        ContentCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="دسته بندی"
    )

    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES,
        verbose_name="نوع محتوا"
    )

    file = models.FileField(
        upload_to="contents/",
        verbose_name="فایل"
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name="نمایش عمومی"
    )

    class Meta:
        verbose_name = "محتوا"
        verbose_name_plural = "محتواها"

class Conversation(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    class Meta:
        verbose_name = "گفتگو"
        verbose_name_plural = "گفتگوها"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        verbose_name="گفتگو"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="فرستنده"
    )

    text = models.TextField(
        blank=True,
        verbose_name="متن"
    )

    attachment = models.FileField(
        upload_to="messages/",
        blank=True,
        null=True,
        verbose_name="فایل"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ارسال"
    )

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

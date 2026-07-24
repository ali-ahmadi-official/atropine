from django.db import models
from multiselectfield import MultiSelectField
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import Student, ConsultantSchedule

class ServiceToStudent(models.Model):
    service = models.CharField(
        max_length=1,
        verbose_name="کد خدمت"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_to_services",
        verbose_name="داوطلب"
    )

    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "خدمت به داوطلب"
        verbose_name_plural = "خدمت ها به داوطلبان"

class Package(models.Model):
    SERVICE_CHOICES = (
        ("1", "جلسه فردی با دکتر نایب زاده"),
        ("2", "جلسه فردی با مشاور"),
        ("3", "تحلیل شخصیت"),
        ("4", "تعیین شانس قبولی"),
        ("5", "پایگاه داده"),
    )

    TYPE_CHOICES = (
        ("1", "برنزی"),
        ("2", "نقره ایی"),
        ("3", "طلایی"),
    )

    service = MultiSelectField(
        max_length=100,
        choices=SERVICE_CHOICES,
        verbose_name="خدمات"
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        verbose_name="نوع پکیج"
    )

    content = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="قیمت به تومان"
    )

    def service_labels(self):
        choices = dict(self.SERVICE_CHOICES)
        return [choices[s] for s in self.service]

    class Meta:
        verbose_name = "پلن"
        verbose_name_plural = "پلن ها"

class PackageRequest(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_packege_requests",
        verbose_name="داوطلب"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="packege_requests",
        verbose_name="پلن"
    )

    final_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ نهایی"
    )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "درخواست پلن"
        verbose_name_plural = "درخواست های پلن"

class Consultation(models.Model):

    service = models.OneToOneField(
        ServiceToStudent,
        on_delete=models.PROTECT,
        related_name="consultation",
        verbose_name="خدمت خریداری شده"
    )

    schedule = models.ForeignKey(
        ConsultantSchedule,
        on_delete=models.CASCADE,
        related_name="schedule_consultations",
        verbose_name="برنامه حضور"
    )

    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "جلسه مشاوره"
        verbose_name_plural = "جلسات مشاوره"

class PaymentStatus(models.TextChoices):
    INIT = "INIT", "ایجاد شده"
    SUCCESS = "SUCCESS", "موفق"
    FAILED = "FAILED", "ناموفق"
    CANCELED = "CANCELED", "لغو شده"

class Payment(models.Model):

    order = models.ForeignKey(
        PackageRequest,
        on_delete=models.CASCADE,
        related_name="order"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    authority = models.CharField(
        max_length=100,
        unique=True
    )

    ref_id = models.CharField(
        max_length=100,
        blank=True
    )

    gateway = models.CharField(
        max_length=50,
        default="zarinpal"
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.INIT
    )

    created_at = models.DateTimeField(auto_now_add=True)

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    tracking_code = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = "فاکتور پرداخت"
        verbose_name_plural = "فاکتور های پرداخت"
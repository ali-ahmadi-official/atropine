from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import User, Student, ConsultantSchedule

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

    def __str__(self):
        return f"پکیج با خدمات: {'، '.join(self.service_labels())}"

    def service_labels(self):
        choices = dict(self.SERVICE_CHOICES)
        return [choices[s] for s in self.service]

    class Meta:
        verbose_name = "پلن"
        verbose_name_plural = "پلن ها"

class DiscountCode(models.Model):
    TYPE_CHOICES = (
        ("percent", "درصدی"),
        ("fixed", "مبلغ ثابت"),
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="کد"
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="نوع تخفیف"
    )

    value = models.PositiveIntegerField(
        verbose_name="مقدار تخفیف"
    )

    max_discount = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="سقف تخفیف"
    )

    packages = models.ManyToManyField(
        Package,
        blank=True,
        verbose_name="پلن‌های مجاز"
    )

    users = models.ManyToManyField(
        User,
        blank=True,
        verbose_name="کاربران مجاز"
    )

    start_at = models.DateTimeField()

    end_at = models.DateTimeField()

    usage_limit = models.PositiveIntegerField(
        default=0,
        help_text="0 یعنی نامحدود"
    )

    usage_count = models.PositiveIntegerField(
        default=0
    )

    per_user_limit = models.PositiveIntegerField(
        default=1
    )

    minimum_amount = models.PositiveIntegerField(
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    apply_to_all_users = models.BooleanField(
        default=False,
        verbose_name="برای همه کاربران"
    )

    apply_to_all_packages = models.BooleanField(
        default=False,
        verbose_name="برای همه پلن‌ها"
    )

    def __str__(self):
        return self.code

    def is_valid(self, user, package, amount):

        now = timezone.now()

        if not self.active:
            return False, "کد غیرفعال است."

        if now < self.start_at:
            return False, "کد هنوز فعال نشده است."

        if now > self.end_at:
            return False, "کد منقضی شده است."

        if self.minimum_amount and amount < self.minimum_amount:
            return False, "حداقل مبلغ خرید رعایت نشده است."

        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False, "ظرفیت کد به پایان رسیده است."

        if self.packages.exists() and package not in self.packages.all():
            return False, "این کد برای این پلن معتبر نیست."

        if self.users.exists() and user not in self.users.all():
            return False, "این کد مخصوص کاربران خاص است."

        if DiscountUsage.objects.filter(
            discount=self,
            user=user
        ).count() >= self.per_user_limit:

            return False, "قبلاً از این کد استفاده کرده‌اید."

        return True, ""

    def calculate_discount(self, amount):

        if self.type == "fixed":

            discount = self.value

        else:

            discount = amount * self.value // 100

            if self.max_discount:

                discount = min(
                    discount,
                    self.max_discount
                )

        return min(discount, amount)

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"

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

    discount_code = models.ForeignKey(
        DiscountCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders"
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "درخواست پلن"
        verbose_name_plural = "درخواست های پلن"

class DiscountUsage(models.Model):

    discount = models.ForeignKey(
        DiscountCode,
        on_delete=models.CASCADE,
        related_name="usages"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    package_request = models.ForeignKey(
        PackageRequest,
        on_delete=models.CASCADE
    )

    used_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "discount",
            "user",
            "package_request"
        )

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

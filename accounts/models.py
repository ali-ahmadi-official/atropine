from datetime import timedelta
from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from .choices import *

class User(AbstractUser):
    ROLE_CHOICES = (
        ("super_admin", "مدیر کل"),
        ("supervisor", "ناظر"),
        ("consultant", "مشاور"),
        ("student", "داوطلب"),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name="نقش")
    mobile = models.CharField(max_length=15, blank=True, unique=True, verbose_name="شماره موبایل")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="تصویر پروفایل")
    is_suspended = models.BooleanField(default=False, verbose_name="تعلیق شده")
    suspension_reason = models.TextField(blank=True, verbose_name="دلیل تعلیق")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_student", verbose_name="کاربر")
    a_completed = models.BooleanField(default=False)
    b_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "داوطلب"
        verbose_name_plural = "داوطلبان"

class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_consultant", verbose_name="کاربر")
    bio = CKEditor5Field(
        "معرفی و توضیحات",
        config_name="default"
    )

    class Meta:
        verbose_name = "مشاور"
        verbose_name_plural = "مشاورین"

class ConsultantSchedule(models.Model):
    consultant = models.ForeignKey(
        Consultant,
        on_delete=models.CASCADE,
        verbose_name="مشاور"
    )

    date = models.DateField(
        verbose_name="تاریخ"
    )

    start_time = models.TimeField(
        verbose_name="ساعت شروع"
    )

    end_time = models.TimeField(
        verbose_name="ساعت پایان"
    )

    class Meta:
        verbose_name = "برنامه حضور مشاور"
        verbose_name_plural = "برنامه های حضور مشاور"

class OTP(models.Model):
    mobile = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils import timezone
        return (
            not self.is_used and
            timezone.now() - self.created_at < timedelta(minutes=2)
        )

class Rank(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="student_rank", verbose_name="داوطلب")

    total_score = models.PositiveIntegerField(verbose_name="نمره کل")
    free_rank = models.PositiveIntegerField(verbose_name="رتبه در سهمیه آزاد")
    quota_5_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='رتبه در سهمیه 5%', help_text="در صورت نداشتن خالی بگذارید")
    quota_25_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='رتبه در سهمیه 25%', help_text="در صورت نداشتن خالی بگذارید")
    quota_city_1_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='رتبه در سهمیه استان محروم 1', help_text="در صورت نداشتن خالی بگذارید")
    quota_city_2_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='رتبه در سهمیه استان محروم 2', help_text="در صورت نداشتن خالی بگذارید")
    sub_group_rank_1 = models.PositiveIntegerField(verbose_name="رتبه در زیرگروه 1")
    sub_group_rank_2 = models.PositiveIntegerField(verbose_name="رتبه در زیرگروه 2")
    sub_group_rank_3 = models.PositiveIntegerField(verbose_name="رتبه در زیرگروه 3")
    sub_group_rank_4 = models.PositiveIntegerField(verbose_name="رتبه در زیرگروه 4")
    sub_group_rank_5 = models.PositiveIntegerField(verbose_name="رتبه در زیرگروه 5")
    report_image = models.ImageField(upload_to="ranks/", verbose_name="تصویر کارنامه", help_text="با مخدوش سازی اطلاعات شخصی")

    class Meta:
        verbose_name = "فرم اطلاعات رتبه سهمیه"
        verbose_name_plural = "فرم های اطلاعات رتبه سهمیه"

class AB(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="student_AB", verbose_name="داوطلب")

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت")
    marital = models.CharField(max_length=1, choices=MARITAL_CHOICES, verbose_name="وضعیت تأهل")
    wife_condition = models.CharField(max_length=1, choices=WIFE_CONDITION_CHOICES, verbose_name="شرایط همسر", null=True, blank=True)
    child = models.CharField(max_length=1, choices=CHILD_CHOICES, verbose_name="فرزند", null=True, blank=True)
    family_support = models.CharField(max_length=1, choices=LEVEL_CHOICES, verbose_name="میزان حمایت خانواده / اطرافیان در صورت ورود به رشته سنگین")
    interest_surgical = models.CharField(max_length=1, choices=LEVEL_CHOICES, verbose_name="علاقه به رشته های جراحی")
    interest_non_surgical = models.CharField(max_length=1, choices=LEVEL_CHOICES, verbose_name="علاقه به رشته های غیر جراحی")
    field_preference = models.CharField(max_length=1, choices=FIELD_PREFERENCE_CHOICES, verbose_name="در رشته های غیر جراحی، کدام فضا را می پسندید؟")
    paraclinic_preference = models.CharField(max_length=1, choices=LEVEL_CHOICES, verbose_name="علاقه به رشته های پاراکلینیک")
    income_importance = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="میزان اهمیت داشتن درآمد بالا")
    residency_free_time_importance = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="اهمیت داشتن تایم آزاد در رزیدنتی")
    career_free_time_importance = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="اهمیت داشتن تایم آزاد در دوران کاری بعد از رزیدنتی")
    no_night_shift_importance = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="اهمیت نداشتن کشیک در رزیدنتی، طرح و پس از آن")
    private_practice_interest = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="تمایل به فعالیت مطب خصوصی به صورت مستقل در آینده")
    academic_interest = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="تمایل به هیئت علمی شدن بعد از اتمام دوران رزیدنتی و طرح")
    immigration_interest = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="تمایل به مهاجرت با تخصص بعد از اتمام دوران رزیدنتی و طرح")
    better_activity = MultiSelectField(choices=SURGERY_CHOICES, max_length=7, verbose_name="در کدام فضا عملکرد بهتری داشتید؟")
    favorite_activity = MultiSelectField(choices=SURGERY_CHOICES, max_length=7, verbose_name="فضاهای کدام رشته‌ها را بیشتر دوست داشتید؟")
    guard = models.CharField(max_length=1, choices=GUARD_CHOICES, verbose_name="کشیک های اینترنی را")

    age = models.PositiveIntegerField(verbose_name="سن", null=True, blank=True)
    city = models.CharField(max_length=200, verbose_name="استان / شهر محل سکونت فعلی", null=True, blank=True)
    university = models.CharField(max_length=200, verbose_name="دانشگاه محل تحصیل دوره پزشکی عمومی", null=True, blank=True)
    taking_assistantship_exam = models.PositiveIntegerField(verbose_name="دفعات شرکت در آزمون دستیاری", null=True, blank=True)
    quota = MultiSelectField(max_length=1, choices=QUOTA_AB_CHOICES, verbose_name="سهمیه اگر دارید انتخاب کنید", null=True, blank=True)
    commitment = MultiSelectField(max_length=1, choices=COMMITMENT_CHOICES, verbose_name="آیا تعهد خاصی برای دوره عمومی دارید؟", null=True, blank=True)
    commitment_other = models.CharField(max_length=255, verbose_name="سایر تعهد دوره عمومی", null=True, blank=True)
    service_status = models.CharField(max_length=1, choices=SERVICE_STATUS_CHOICES, verbose_name="وضعیت طرح", null=True, blank=True)
    service_location = models.CharField(max_length=1, choices=SERVICE_LOCATION_CHOICES, verbose_name="محل انجام طرح", null=True, blank=True)
    service_location_other = models.CharField(max_length=255, verbose_name="سایر محل انجام طرح", null=True, blank=True)
    military_status = models.CharField(max_length=1, choices=MILITARY_STATUS_CHOICES,verbose_name="وضعیت سربازی", null=True, blank=True)
    field_selection_importance = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="انتخاب رشته مناسب برای شما چقدر مهم است", null=True, blank=True)
    favorite_specialties = models.TextField(verbose_name="رشته‌های مورد قبول شما برای رزیدنتی (به ترتیب اولویت)", null=True, blank=True)
    unacceptable_specialties = models.TextField(verbose_name="رشته‌هایی که اصلاً انتخاب نمی‌کنید", null=True, blank=True)
    city_priority_importance = models.CharField(max_length=2, choices=NUMBER_CHOICES, verbose_name="اولویت شهر برای شما چقدر مهم است", null=True, blank=True)
    favorite_universities = models.TextField(verbose_name="دانشگاه‌های مورد قبول شما برای رزیدنتی (به ترتیب اولویت)", null=True, blank=True)
    unacceptable_universities = models.TextField(verbose_name="دانشگاه‌هایی که اصلاً انتخاب نمی‌کنید", null=True, blank=True)
    biggest_challenge = models.TextField(verbose_name="بزرگ‌ترین چالش شما در انتخاب رشته چیست؟", null=True, blank=True)
    additional_notes = models.TextField(verbose_name="هر نکته مهمی که فکر می‌کنید در انتخاب رشته شما موثر است", null=True, blank=True)

    class Meta:
        verbose_name = "فرم اطلاعات A و B"
        verbose_name_plural = "فرم های اطلاعات A و B"

    def a_save(self):
        result = super().save()
        self.student.a_completed = True
        self.student.save(update_fields=["a_completed"])
        return result
    
    def b_save(self):
        result = super().save()
        self.student.b_completed = True
        self.student.save(update_fields=["b_completed"])
        return result

class Personality60(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="student_personality_60", verbose_name="داوطلب")

    q1 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از گفت‌وگوی مستقیم با بیمار و شنیدن شرح حال او لذت می‌برم.")
    q2 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="ترجیح می‌دهم بخش زیادی از زمان کاری‌ام در ارتباط رو‌در‌رو با بیمار بگذرد.")
    q3 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="اگر در یک رشته ارتباطم با بیمار بسیار محدود باشد، احتمالاً از آن کمتر رضایت خواهم داشت.")
    q4 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="رنج یا نگرانی بیمار معمولاً بر من اثر عاطفی می‌گذارد.")
    q5 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="وقتی بیمار یا خانواده‌اش ناراحت هستند، معمولاً با آن‌ها هم‌حس می‌شوم.")
    q6 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="می‌توانم بدون درگیر شدن عاطفی، نسبت به مشکلات بیمار کاملاً فاصله‌دار بمانم.")
    q7 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="در موقعیت‌های اورژانسی یا بحرانی، معمولاً می‌توانم تمرکزم را حفظ کنم.")
    q8 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="وقتی لازم باشد در زمان کوتاه تصمیم مهمی بگیرم، عملکردم معمولاً حفظ می‌شود.")
    q9 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="فضاهای پرتنش و سریع معمولاً آن‌قدر مرا آشفته می‌کنند که کارایی‌ام پایین می‌آید.")
    q10 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="وقتی چند مسئله مهم هم‌زمان پیش می‌آید، معمولاً می‌توانم سریع اولویت‌بندی کنم.")
    q11 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="اگر یک رشته به‌طور مداوم حجم کاری بالایی داشته باشد، معمولاً می‌توانم با آن کنار بیایم.")
    q12 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="تحمل یک برنامه کاری فشرده در بلندمدت برایم دشوار است.")
    q13 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="می‌توانم بپذیرم که بعضی مسیرهای شغلی برای مدت طولانی انرژی زیادی از من بگیرند.")
    q14 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="ایستادن طولانی‌مدت حین کار معمولاً برایم خیلی آزاردهنده نیست.")
    q15 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="کشیک‌های شبانه و کم‌خوابی معمولاً خیلی زود توانم را کم می‌کنند.")
    q16 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از نظر بدنی می‌توانم خودم را با محیط‌های کاری سنگین و طولانی تطبیق دهم.")
    q17 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از انجام کارهای عملی و اجرایی بیشتر از کارهای صرفاً فکری لذت می‌برم.")
    q18 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="وقتی بتوانم با دست خودم یک اقدام مشخص انجام دهم، احساس رضایت بیشتری دارم.")
    q19 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="کارهایی که به مهارت دستی و اجرای دقیق نیاز دارند، برایم جذاب هستند.")
    q20 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="ترجیح می‌دهم بیشتر در نقش تحلیل‌گر باشم تا اجراکننده.")
    q21 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از کارهایی که به دقت بالا و توجه به جزئیات نیاز دارند، لذت می‌برم.")
    q22 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="برای انجام کارهای ظریف، معمولاً صبر و تمرکز کافی دارم.")
    q23 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="کارهای بسیار دقیق و ریز معمولاً برایم خسته‌کننده هستند.")
    q24 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از کنار هم گذاشتن نشانه‌ها و رسیدن به تشخیص درست لذت می‌برم.")
    q25 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="پرونده‌های پیچیده‌ای که به تحلیل چندمرحله‌ای نیاز دارند، برایم جذاب‌اند.")
    q26 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="یکی از بخش‌های جذاب پزشکی برایم فهمیدن علت اصلی مشکل بیمار است.")
    q27 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="وقتی پاسخ یک مسئله بالینی فوراً روشن نباشد، معمولاً زود خسته می‌شوم.")
    q28 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="اگر پاسخ یک مسئله بالینی از ابتدا روشن نباشد، معمولاً می‌توانم آرام بمانم.")
    q29 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="در موقعیت‌هایی که هنوز همه‌چیز قطعی نیست، می‌توانم به کار ادامه دهم.")
    q30 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="ابهام در تشخیص یا مسیر درمان معمولاً مرا بیش از حد مضطرب می‌کند.")
    q31 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="دوست دارم نتیجه اقدام درمانی را در زمان نسبتاً کوتاه ببینم.")
    q32 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="برایم رضایت‌بخش است که اثر کارم نسبتاً سریع و واضح دیده شود.")
    q33 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="روندهای درمانی طولانی و تدریجی معمولاً برایم خسته‌کننده هستند.")
    q34 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از این‌که بیمار را در طول زمان پیگیری کنم و روند او را ببینم، لذت می‌برم.")
    q35 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="همراهی طولانی‌مدت با بیمار برایم ارزشمند است.")
    q36 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="ترجیح می‌دهم پس از یک مداخله کوتاه، دیگر درگیر ادامه مسیر بیمار نباشم.")
    q37 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="در محیط‌هایی که نیاز به هماهنگی مداوم با اعضای تیم درمان دارند، راحت هستم.")
    q38 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از کار کردن در کنار همکاران و پیش بردن مشترک فرایند درمان لذت می‌برم.")
    q39 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="ترجیح می‌دهم بیشتر کارها را به‌تنهایی و بدون وابستگی به دیگران انجام دهم.")
    q40 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="برایم مهم است که در تصمیم‌گیری‌های حرفه‌ای، استقلال قابل‌توجهی داشته باشم.")
    q41 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="محیط‌هایی را ترجیح می‌دهم که در آن‌ها بتوانم سبک کاری خودم را بیشتر تعیین کنم.")
    q42 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="اگر ساختار کاری بسیار از پیش تعیین‌شده باشد، معمولاً احساس محدودیت می‌کنم.")
    q43 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="برایم مهم است که شغلم زمان کافی برای زندگی شخصی باقی بگذارد.")
    q44 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="تمایلی ندارم برای سال‌های طولانی، تقریباً تمام زندگی شخصی‌ام را فدای کار کنم.")
    q45 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="داشتن برنامه کاری نسبتاً قابل‌پیش‌بینی برای من یک مزیت مهم است.")
    q46 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="اگر رشته‌ای را خیلی دوست داشته باشم، به‌هم‌خوردن شدید نظم زندگی شخصی برایم مسئله مهمی نیست.")
    q47 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="از مطالعه عمیق و به‌روز ماندن علمی لذت می‌برم.")
    q48 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="تدریس، آموزش یا مشارکت در فعالیت‌های علمی برایم جذاب است.")
    q49 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="رشته‌هایی که به مطالعه مداوم و جدی نیاز دارند، معمولاً برایم خسته‌کننده‌اند.")
    q50 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="کار کردن با دستگاه‌ها، تجهیزات و فناوری‌های پزشکی برایم جذاب است.")
    q51 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="در محیط‌های کاریِ وابسته به ابزار و فناوری، معمولاً احساس راحتی می‌کنم.")
    q52 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="اگر یک رشته بیش از حد به تجهیزات و فناوری وابسته باشد، علاقه‌ام به آن کمتر می‌شود.")
    q53 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="کار با کودکان و نوزادان برایم به‌طور خاص لذت‌بخش است.")
    q54 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="برقراری ارتباط با کودک و خانواده او برایم جذابیت ویژه‌ای دارد.")
    q55 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="گوش دادن به مسائل ذهنی، رفتاری و عاطفی بیماران برایم جذاب است.")
    q56 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="حوزه‌هایی که بر فهم ذهن، رفتار و هیجان انسان تمرکز دارند، برایم کشش ویژه‌ای دارند.")
    q57 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="دیدن خون، آسیب شدید یا صحنه‌های تهاجمی پزشکی معمولاً تمرکزم را به‌هم نمی‌زند.")
    q58 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="مواجهه با صحنه‌های خشن پزشکی معمولاً آن‌قدر مرا ناراحت می‌کند که ترجیح می‌دهم از آن فضا دور بمانم.")
    q59 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="به رشته‌هایی علاقه دارم که در آن‌ها بتوان مشکل را با اقدام مستقیم و فعال تغییر داد.")
    q60 = models.CharField(max_length=1, choices=LIKERT_CHOICES, verbose_name="مدیریت محافظه‌کارانه و صرفاً پیگیری طولانی، برایم از مداخله مستقیم جذاب‌تر است.")

    class Meta:
        verbose_name = "فرم تحلیل شخصیت 60 سوالی"
        verbose_name_plural = "فرم های تحلیل شخصیت 60 سوالی"

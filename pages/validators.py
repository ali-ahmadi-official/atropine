from django.core.exceptions import ValidationError
import os

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".m4v",
    ".mpeg",
    ".mpg",
    ".wmv",
}


def validate_video(value):
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in VIDEO_EXTENSIONS:
        raise ValidationError(
            "فقط فایل‌های ویدیویی مجاز هستند."
        )
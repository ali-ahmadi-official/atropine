from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Student, Consultant


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == "consultant":
        Consultant.objects.create(user=instance)

    elif instance.role == "student":
        Student.objects.create(user=instance)
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def user_profile_creation(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()

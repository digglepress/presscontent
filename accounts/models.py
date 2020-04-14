from django.contrib.auth import get_user_model
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ProcessedImageField(default='profile_avatar.png',
                                 upload_to='users_avatar', format='png',
                                 processors=[ResizeToFill(50, 50)],
                                 options={'quality': 80}, blank=True)
    avatar_large = ImageSpecField(source='avatar',
                                  format='png',
                                  processors=[ResizeToFill(100, 100)],
                                  options={'quality': 80})
    bio = models.TextField(max_length=200, blank=True)
    profession = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)

    def __str__(self):
        user_detail = '{} ({})'.format(self.user.username, self.user.email)
        return user_detail

    def get_location(self):
        return '{}, {}'.format(self.city, self.country)


class Social(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook = models.URLField()
    twitter = models.URLField()
    instagram = models.URLField()

    def __str__(self):
        return '{} {}'.format(self.user.get_full_name, 'socials')

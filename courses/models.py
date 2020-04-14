from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from courses.utilities import course_slug
from django.db.models.signals import pre_save
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from tinymce.models import HTMLField

User = get_user_model()


class Courses(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = ProcessedImageField(upload_to='courses_featured_image', processors=[ResizeToFill(600, 300)],
                                format='png', options={'quality': 80}, blank=True)
    cover_sm = ImageSpecField(source='cover',
                              processors=[ResizeToFill(600, 600)],
                              format='png',
                              options={'quality': 100})
    slug = models.SlugField()
    title = models.CharField(max_length=200)
    body = HTMLField()
    # body = models.TextField()
    summary = models.CharField(max_length=300)
    published = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return '{} {}'.format(self.author.username, self.title)

    def get_absolute_url(self):
        return reverse('course:course_detail', kwargs={'slug': self.slug})


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = course_slug(instance, instance.title, instance.slug)


pre_save.connect(slug_save, sender=Courses)


class Comments(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reply')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-commented_at',)
        verbose_name_plural = 'Comments'

    def __str__(self):
        return "{}".format(self.author)

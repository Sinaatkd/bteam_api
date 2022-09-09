from django.db import models
from django.utils.timezone import now
from datetime import timedelta

from account.models import User
from utilities import get_filename_ext


def story_upload_path(instance, filepath):
    name, ext = get_filename_ext(filepath)
    new_name = f'{instance.user.full_name}-{instance.pk}'
    path = f'stories/{instance.user.full_name}/{new_name}{ext}'
    return path


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    story_file = models.FileField(upload_to=story_upload_path)
    expire_time = models.DateTimeField(default=now() + timedelta(days=1))
    visitors = models.ManyToManyField(User, blank=True)
    
    def __str__(self) -> str:
        return f'{self.user.full_name}-{self.pk}'
    
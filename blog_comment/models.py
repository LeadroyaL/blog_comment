from django.db import models
from django.utils import timezone


class Comment(models.Model):
    post_ID = models.IntegerField()
    author = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    content = models.CharField(max_length=1024 * 1024)
    time = models.DateTimeField(default=timezone.now)
    is_reviewed = models.BooleanField(default=False)

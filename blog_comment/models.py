from django.db import models


class Comment(models.Model):
    post_ID = models.IntegerField()
    author = models.CharField(max_length=128)
    email = models.EmailField()
    content = models.CharField(max_length=1024 * 1024)
    time = models.DateField(auto_now=True)
    is_reviewed = models.BooleanField(default=False)

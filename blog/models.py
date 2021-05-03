from django.db import models
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=False)
    date_time = models.DateTimeField(default=timezone.now())

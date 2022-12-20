from django.db import models
from django.utils import timezone


# Create your models here.

class Video(models.Model):
    upload_date = models.DateTimeField(default=timezone.now)
    session_id = models.CharField(blank=True, max_length=255)
    file_url = models.CharField(blank=True, max_length=255)

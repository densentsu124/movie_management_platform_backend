from django.db import models
import json
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to="videos/", null=True, verbose_name="")
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, verbose_name="")

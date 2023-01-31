from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='covers')
    votes = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

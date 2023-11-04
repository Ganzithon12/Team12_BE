from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def user_photo_path(instance, filename):
    return f'profile_image/{instance.member.pk}/{filename}'

class CustomUser(AbstractUser):
  REQUIRED_FIELDS = []
  email = None
  nickname = models.CharField(max_length=100)
  profile_image = models.ImageField(upload_to=user_photo_path, null = True)

  def __str__(self):
    return self.nickname
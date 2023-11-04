from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
def user_photo_path(instance, filename):
    return f'profile_image/{filename}'

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    nickname = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=user_photo_path, null = True, blank = True)

    groups = models.ManyToManyField(Group, related_name='custom_users_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users_permissions')

    def __str__(self):
        return self.nickname
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

# Create your models here.
def user_photo_path(instance, filename):
    return f'profile_image/{filename}'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('must have user username')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    # email = None
    email = models.EmailField(default='', null=False, blank=False, unique=True)
    nickname = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=user_photo_path, null = True, blank = True)
    point = models.IntegerField(default=10000)

    groups = models.ManyToManyField(Group, related_name='custom_users_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users_permissions')

    def __str__(self):
        return self.nickname
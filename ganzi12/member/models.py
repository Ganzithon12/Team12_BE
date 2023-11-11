from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, BaseUserManager
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    # 일반 user 생성
    
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
            password = password,
            **extra_fields
        )
        user.save(using=self._db)
        return user
    
    # 관리자 user 생성
    def create_superuser(self, email, nickname, password=None):
        user = self.create_user(
            email = email,
            password = make_password(password),
            nickname= nickname,
        )
        token = Token.objects.create(user=user)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(max_length=100)
    profile_image = models.ImageField(verbose_name='profile_image', upload_to='profile_image', null = True, blank = True)
    point = models.IntegerField(default=10000)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
       return self.is_admin

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='custom_users_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users_permissions')

    def __str__(self):
        return self.nickname
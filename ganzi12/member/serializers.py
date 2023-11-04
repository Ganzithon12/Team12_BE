from rest_framework import serializers
from .models import *

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname', 'profile_image']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'password', 'nickname', 'profile_image']
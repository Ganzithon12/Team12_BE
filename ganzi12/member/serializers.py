from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'nickname', 'profile_image', 'point']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'nickname', 'profile_image']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        User = get_user_model()

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return data
        raise serializers.ValidationError('Incorrect email or password')


class UserInfoSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'profile_image', 'point']
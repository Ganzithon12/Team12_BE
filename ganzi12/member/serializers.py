from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname', 'profile_image']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'nickname', 'profile_image']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        User = get_user_model()

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return data
        raise serializers.ValidationError('Incorrect username or password')


class UserInfoSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'profile_image']
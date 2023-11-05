from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token 


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'nickname', 'profile_image', 'point']


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2', 'nickname', 'profile_image']

    def validate(self, data):
        if data['password']!= data['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords don't match."})
        return data
    
    def create(self, validated_data):
        password = validated_data['password']
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=password  # 사용자가 입력한 패스워드를 사용
        )

        print(f"New user email: {user.email}")
        print(f"New user password: {validated_data['password']}")

        token = Token.objects.create(user=user)
        return user

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        User = get_user_model()

        user = authenticate(request=self.context['request'], email=email, password=password)
        if user:
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
        fields = ['id', 'nickname', 'profile_image', 'point']
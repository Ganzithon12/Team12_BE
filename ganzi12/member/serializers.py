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
        profile_image = validated_data.pop('profile_image', None)

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=password
        )

        if profile_image:
            user.profile_image = profile_image
            user.save()


        print(f"New user email: {user.email}")
        print(f"New user profile_image: {user.profile_image}")
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

    def update(self, instance, validated_data):
        instance.point = validated_data.get('point', instance.point)
        instance.save()
        return instance  
    
    def get_profile_image(self, obj):
        if self.context and 'request' in self.context:
            request = self.context['request']
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None

    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'profile_image', 'point']
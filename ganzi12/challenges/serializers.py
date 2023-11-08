from rest_framework import serializers
from .models import *
from member.serializers import UserInfoSerializer

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        exclude = ['challengers']

class ChallengeCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeCompleted
        fields = '__all__'

class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
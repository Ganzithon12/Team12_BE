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
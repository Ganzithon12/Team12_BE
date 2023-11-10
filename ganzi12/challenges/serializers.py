from rest_framework import serializers
from .models import *
from member.serializers import UserInfoSerializer

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        # exclude = ['challengers']
        fields = ['title', 'entry_fee', 'start_at', 'finish_at', 'challenge_logo', 'maximum_num']

class ChallengeCompletedSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.nickname')

    class Meta:
        model = ChallengeCompleted
        fields = '__all__'

class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
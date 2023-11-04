from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from member.models import CustomUser
from member.serializers import CustomUserDetailSerializer


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = ['mission_id', 'title', 'point', 'mission_logo']

class CompletedSerializer(ModelSerializer):
    mission = serializers.ReadOnlyField(source = 'mission.title')
    writer = serializers.ReadOnlyField(source = 'writer.nickname')

    class Meta:
        model = MissionCompleted
        fields = ['mission_image', 'status', 'completion_date']
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from member.serializers import UserInfoSerializer


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = ['mission_id', 'title', 'point', 'mission_logo']

class CompletedSerializer(ModelSerializer):
    class UserInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model=CustomUser
            fields=['nickname', 'point']
            
    mission = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all())
    writer = serializers.ReadOnlyField(source='writer.nickname')
    status = serializers.BooleanField(default=True, read_only=True)
    created_at = serializers.DateTimeField(default=timezone.now, read_only=True)

    class Meta:
        model = MissionCompleted
        fields = ['mission', 'mission_image', 'writer', 'status', 'created_at']
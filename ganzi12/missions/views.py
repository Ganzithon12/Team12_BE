from .models import Mission, MissionCompleted
from .serializers import MissionSerializer, CompletedSerializer
from member.serializers import UserInfoSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import permissions

class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    

class CompletedViewSet(ModelViewSet):
    queryset = MissionCompleted.objects.all()
    serializer_class = CompletedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        mission_id = self.kwargs['mission_id']
        mission = get_object_or_404(Mission, mission_id=mission_id)
        loginUser = self.request.user
        loginUser.point += mission.point
        loginUser.save()

        serializer.save(
            mission=mission,
            writer=loginUser,
            status=True,
        )

    def get_queryset(self, **kwargs): # Override
        mission_id = self.kwargs['mission_id']
        return self.queryset.filter(mission_id=mission_id, writer=self.request.user)
from .models import Mission, MissionCompleted
from .serializers import MissionSerializer, CompletedSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    

class CompletedViewSet(ModelViewSet):
    queryset = MissionCompleted.objects.all()
    serializer_class = CompletedSerializer

    def perform_create(self, serializer):
        mission_id = self.kwargs['mission_id']
        mission = get_object_or_404(Mission, mission_id=mission_id)
        loginUser = self.request.user
        serializer.save(
            mission=mission,
            writer=loginUser,
            status=True,
        )

    def get_queryset(self, **kwargs): # Override
        mission_id = self.kwargs['mission_id']
        return self.queryset.filter(mission_id=mission_id)
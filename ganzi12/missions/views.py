from .models import Mission, MissionCompleted
from member.models import CustomUser
from .serializers import MissionSerializer, CompletedSerializer
from member.serializers import CustomUserDetailSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet


class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
from .models import Mission, MissionCompleted
from .serializers import MissionSerializer, CompletedSerializer
from member.serializers import UserInfoSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView


class MissionViewSet(ModelViewSet):
    """
    mission 생성 view
    """
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    # permission_classes = [permissions.IsAdminUser]
    

class CompletedViewSet(ModelViewSet):
    """
    mission 인증 글 작성 view
    """
    queryset = MissionCompleted.objects.all()
    serializer_class = CompletedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        mission_id = self.kwargs['mission_id']
        mission = get_object_or_404(Mission, mission_id=mission_id)
        loginUser = self.request.user
        today_completed = MissionCompleted.objects.filter(mission=mission, writer=loginUser, created_at__date=timezone.now().date()).first()

        if today_completed:
            return Response({"detail": "하루에 한 번만 미션 인증을 작성할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        loginUser.point += mission.point
        loginUser.save()

        serializer.save(
            mission=mission,
            writer=loginUser,
        )

    def get_queryset(self):
        mission_id = self.kwargs['mission_id']
        return self.queryset.filter(mission_id=mission_id, writer=self.request.user)

class CompletedListView(APIView):
    """
    내가 인증한 미션 list 조회
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loginUser = self.request.user
        completed_missions = MissionCompleted.objects.filter(writer=loginUser)
        serializer = CompletedSerializer(completed_missions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
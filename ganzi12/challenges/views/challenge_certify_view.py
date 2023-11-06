from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.utils import timezone

class CreateCertify(CreateAPIView):
    """
    챌린지 인증 view
    """
    serializer_class = ChallengeCompletedSerializer
    queryset = ChallengeCompleted
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        challenge_id = self.kwargs['challenge_id']
        challenge = Challenge.objects.get(pk = challenge_id)
        user = self.request.user
        if ChallengeCompleted.objects.filter(challenge = challenge, writer = user, created_at = timezone.now().date()).exists():
            res = {
                "msg" : "이미 인증한 챌린지",
                "code" : "F-C003"
            }
            return Response(res)
        
        serializer.save(challenge = challenge, writer = user)
        res = {
            "msg" : "챌린지 인증 성공",
            "code" : "S-C002"
        }
        return Response(res)
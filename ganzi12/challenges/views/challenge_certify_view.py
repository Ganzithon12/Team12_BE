from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.utils import timezone

class CreateCertify(APIView):
    """
    챌린지 인증 view
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, challenge_id):
        # challenge_id = self.kwargs['challenge_id']
        challenge = Challenge.objects.get(pk = challenge_id)
        user = self.request.user
        if ChallengeCompleted.objects.filter(challenge = challenge, writer = user, created_at = timezone.now().date()).exists():
            res = {
                "msg" : "이미 인증한 챌린지",
                "code" : "F-C003"
            }
            return Response(res)
        try:
            certification = ChallengeCompleted(writer = user, challenge = challenge, challenge_image = request.data['challenge_image'])
            certification.save()
            res = {
                "msg" : "챌린지 인증 성공",
                "code" : "S-C002"
            }
            return Response(res)
        except:
            res = {
                "msg" : "잘못된 요청",
                "code" : "F-C008"
            }
            return Response(res)
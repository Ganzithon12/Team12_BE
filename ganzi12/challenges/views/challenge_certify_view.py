from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
        

class CertifyList(APIView):
    """
    특정 챌린지에 대한 인증 조회
    """
    
    def get(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, pk = challenge_id)
        certifies = ChallengeCompleted.objects.filter(challenge = challenge)
        certifies_list = ChallengeCompletedSerializer(certifies, many = True).data
        if certifies_list:
            res = {
                "msg" : "챌린지 인증 조회 성공",
                "code" : "S-C006",
                "data" : certifies_list
            }
        else:
            res = {
                "msg" : "해당 챌린지에 등록된 인증 없음",
                "code" : "S-C007"
            }
        
        return Response(res)
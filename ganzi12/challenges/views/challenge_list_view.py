from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

class ChallengeList(APIView):
    """
    챌린지 목록
    """
    def get(self, request, state):
        # state = self.kwargs['state']
        now = timezone.now().date()
        if state == "pre":
            challenges = Challenge.objects.filter(start_at__gt = now)
            msg = "참가 가능한 챌린지 불러오기 성공"
        elif state == "now":
            challenges = Challenge.objects.filter(Q(start_at__lt = now)&Q(finish_at__gt = now))
            msg = "진행중인 챌린지 불러오기 성공"
        elif state == "post":
            challenges = Challenge.objects.filter(finish_at__lt = now)
            msg = "종료된 챌린지 불러오기 성공"
        else:
            res = {
                "msg" : "잘못된 요청 값",
                "code" : "F-C007"
            }
            return Response(res)
        
        serializer = ChallengeSerializer(challenges, many = True)
        res = {
            "msg" : msg,
            "code" : "S-C004",
            "data" : serializer.data
        }
        return Response(res)


class ChallengeInfo(APIView):
    """
    특정 챌린지 정보 조회 view
    """
    authentication_classes = [JWTAuthentication]

    def get(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, pk = challenge_id)
        challenge_info = ChallengeDetailSerializer(challenge).data
        
        user = self.request.user
        if challenge.challengers.filter(pk = user.pk).exists():
            participated = True
        else:
            participated = False
        data = {}

        data.update({"participated" : participated, "challenge_info" : challenge_info})
        
        res = {
            "msg" : "챌린지 조회 성공",
            "code" : "S-C004",
            "data" : data
        }
        
        return Response(res)
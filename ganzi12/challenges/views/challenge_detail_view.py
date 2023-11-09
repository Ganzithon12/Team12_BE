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
from datetime import date

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
            "code" : "S-C005",
            "data" : data
        }
        
        return Response(res)
    

class ChallengersInfoList(APIView):
    """
    해당 챌린지에 참여중인 유저들의 리스트
    """
    def get(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, pk = challenge_id)
        today = date.today()
        max_cnt = challenge.period
        if (challenge.finish_at - today).days < 0:
            # 이미 종료된 챌린지
            days = "-1"
        elif (today - challenge.start_at).days < 0:
            # 아직 시작하지 않은 챌린지
            res = {
                "msg" : "아직 시작하지 않은 챌린지",
                "code" : "S-C008"
            }
            return Response(res)
        else:
            days = (today - challenge.start_at).days + 1
        
        user_list = []
        users = challenge.challengers.all()
        certifies = ChallengeCompleted.objects.filter(challenge__pk = challenge_id)
        for u in users:
            user_data = UserInfoSerializer(u).data
            certifies_cnt = certifies.filter(writer = u).count()
            user_data.update({"cnt" : certifies_cnt})
            user_list.append(user_data)

        data = {
            "days" : days,
            "max_cnt" : max_cnt,
            "user_list" : user_list
        }

        res = {
            "msg" : "챌린지 참가자들의 정보 불러오기 성공",
            "code" : "S-009",
            "data" : data
        }

        return Response(res)
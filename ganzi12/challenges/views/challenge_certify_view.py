from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Q

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
    

class MyCertifies(APIView):
    """
    내 인증 개수
    """
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, challenge_id):
        user = self.request.user
        challenge = get_object_or_404(Challenge, pk = challenge_id)

        cnt = ChallengeCompleted.objects.filter(Q(challenge = challenge)&Q(writer = user)).count()

        res = {
            "msg" : "유저의 인증 개수 불러오기 성공",
            "code" : "S-010",
            "data" : {
                "cnt" : cnt
            }
        }

        return Response(res)
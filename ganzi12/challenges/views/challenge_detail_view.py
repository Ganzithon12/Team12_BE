from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

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
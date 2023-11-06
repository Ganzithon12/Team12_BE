from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

class ParticipateChallenge(APIView):
    """
    챌린지에 참가하는 view
    """
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, challenge_id):
        challenge = Challenge.objects.get(pk = challenge_id)
        user = self.request.user

        if challenge.challengers.filter(pk = user.pk).exists():
            res = {
                "msg" : "이미 참가 중인 사용자",
                "code" : "F-C004"
            }
            return Response(res)
        
        if challenge.maximum_num <= challenge.current_num:
            res = {
                "msg" : "참가 인원 초과",
                "code" : "F-C005"
            }
            return Response(res)
        
        if user.point < challenge.entry_fee:
            res = {
                "msg" : "참가 포인트 부족",
                "code" : "F-C006"
            }
            return Response(res)

        challenge.challengers.add(user)
        challenge.current_num += 1
        challenge.sum_point += challenge.entry_fee
        challenge.save()
        
        user.point -= challenge.entry_fee
        user.save()
        
        res = {
            "msg" : "챌린지 참가 성공",
            "code" : "S-C003"
        }
        return Response(res)




from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class ChallengeViewSet(ModelViewSet):
    """
    챌린지 생성 view
    """
    # authentication_classes = [JWTAuthentication]
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def create(self, request):
        user = self.request.user
        # if not user.is_admin:
        #     res = {
        #         "msg" : "관리자가 아닌 사용자 접근",
        #         "code" : "F-C001"
        #     }
        #     return Response(res)
        
        serializer = ChallengeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            res = {
                "msg" : "새로운 챌린지 등록 성공",
                "code" : "S-C001"
            }
            return Response(res)
        res = {
            "msg" : "잘못된 요청",
            "code" : "F-C002",
            "errors" : serializer.errors
        }
        return Response(res)
    
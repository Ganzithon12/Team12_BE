from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def user_info(request):
    serializer = UserInfoSerializer(request.user)
    data = serializer.data
    if data["nickname"] == None:
        res = {
            "msg" : "유저 정보 불러오기 실패",
        }
        return Response(res)
    res = {
        "msg" : "유저 정보 불러오기 성공",
        "data" : data
    }
    return Response(res)
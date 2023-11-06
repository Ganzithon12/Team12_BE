from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def user_info(request):
    """
    유저 정보 불러오는 view
    """
    serializer = UserInfoSerializer(request.user)
    data = serializer.data
    res = {
        "msg" : "유저 정보 불러오기 성공",
        "code" : "S-M003",
        "data" : data
    }
    return Response(res)
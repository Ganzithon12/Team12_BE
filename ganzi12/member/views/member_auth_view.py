from ..models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        if CustomUser.objects.filter(username = request.data.get('username')).exists():
            res = {
                "msg" : "이미 존재하는 회원 ID",
                "code" : "F-M001",
            }
            return Response(res)
        
        if CustomUser.objects.filter(nickname = request.data.get('nickname')).exists():
            res = {
                "msg" : "이미 존재하는 회원 닉네임",
                "code" : "F-M002",
            }
            return Response(res)
        
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])
            new_user = serializer.save(password = password)
            
            token = TokenObtainPairSerializer.get_token(new_user)
            
            res = {
                "msg" : "회원가입 성공",
                "code" : "S-M001",
                "data" : {
                    "access_token" : str(token.access_token)
                }
            }
            return Response(res)

        res = {
            "msg" : "회원가입 실패",
            "code" : "F-M003",
        }
        return Response(res)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']
            res = {
                "msg": "로그인 성공",
                "code" : "S-M002",
                "data": {
                    "access_token" : access_token
                }
            }
            return Response(res)
        res = {
            "msg" : "로그인 실패",
            "code" : "F-M004",
        }
        return Response(res)
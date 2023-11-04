from ..models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from django.contrib import auth
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save(password = make_password(serializer.validated_data['password']))
        auth.login(request, new_user)
        user_data = CustomUserDetailSerializer(new_user)
        res = {
            "msg" : "회원가입 성공",
            "data" : user_data.data
        }
        return Response(res)
    res = {
        "msg" : "회원가입 실패"
    }
    return Response(res)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = auth.authenticate(
            request=request,
            username=serializer.data['username'],
            password=serializer.data['password']
        )
        if user is not None:
            auth.login(request, user)
            user_data = CustomUserDetailSerializer(user)
            res = {
                "msg" : "로그인 성공",
                "data" : user_data.data
            }
            return Response(res)
        res = {
            "msg" : "존재하지 않는 회원"
        }
        return Response(res)
    res = {
        "msg" : "잘못된 요청"
    }
    return Response(res)


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    res = {
        "msg" : "로그아웃 성공"
    }
    return Response(res)
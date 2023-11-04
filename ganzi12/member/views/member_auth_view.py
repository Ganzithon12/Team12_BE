from ..models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView

# @api_view(['POST'])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         new_user = serializer.save(password = make_password(serializer.validated_data['password']))
#         auth.login(request, new_user)
#         user_data = CustomUserDetailSerializer(new_user)
#         res = {
#             "msg" : "회원가입 성공",
#             "data" : user_data.data
#         }
#         return Response(res)
#     res = {
#         "msg" : "회원가입 실패"
#     }
#     return Response(res)

class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        if CustomUser.objects.filter(username = request.data.get('username')).exists():
            res = {
                "msg" : "이미 존재하는 회원 ID"
            }
            return Response(res)
        
        if CustomUser.objects.filter(nickname = request.data.get('nickname')).exists():
            res = {
                "msg" : "이미 존재하는 회원 닉네임"
            }
            return Response(res)
        
        # password = request.data.get('password')
        # hashed_password = make_password(password)
        # request.data['password'] = hashed_password
        
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            new_user = serializer.save(password = make_password(serializer.validated_data['password']))
            auth.login(request, new_user)

            user_info = UserInfoSerializer(new_user, context={'request': self.request})
            
            res = {
                "msg" : "회원가입 성공",
                "data" : user_info.data
            }
            return Response(res)

        res = {
            "msg" : "회원가입 실패",
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
            user_data = UserInfoSerializer(user, context={'request': request})
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
from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q

class Calculate(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request, challenge_id): # 완료된 챌린지 id
        now = timezone.now().date()
        challenge = get_object_or_404(Challenge, pk = challenge_id)
        created_at = ChallengeCompleted.objects.filter(challenge=challenge)['created_at']
        total = challenge['sum_point']
        success_challenger = 0
        users = challenge.challengers
        for user in users:
            max_cnt = challenge.finish_at - challenge.start_at
            cnt = ChallengeCompleted.objects.filter(Q(challenge = challenge)&Q(writer = user)&(Q(start_at__gt = created_at)&Q(finish_at__lt = created_at))).count()
            if cnt == max_cnt:
                success_challenger += 1
        give_point = total / success_challenger
        for user in users:
            max_cnt = challenge.finish_at - challenge.start_at
            cnt = ChallengeCompleted.objects.filter(Q(challenge = challenge)&Q(writer = user)&(Q(start_at__gt = created_at)&Q(finish_at__lt = created_at))).count()
            if cnt == max_cnt:
                user.point += give_point
        return Response(status=status.HTTP_200_OK)



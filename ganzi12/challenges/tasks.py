from rest_framework.response import Response
from .serializers import *
from .models import *
from member.models import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, status
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Q

def calc_point(challenge):
    total = challenge.sum_point
    winner = 0
    winner_lst = []
    loser_lst = []
    users = challenge.challengers.all()
    certifies = ChallengeCompleted.objects.filter(challenge = challenge)

    for user in users:
        cnt = certifies.filter(writer = user).count()
        if cnt == challenge.period:
            winner += 1
            winner_lst.append(user.pk)
        else:
            loser_lst.append(user.pk)
    
    prize_point = int(total / winner)

    for i in winner_lst:
        u = CustomUser.objects.get(pk = i)
        u.point += prize_point
        u.save()
    
    return {
        "challenge_id" : challenge.pk,
        "prize_point" : prize_point,
        "winner_lst" : winner_lst,
        "loser_lst" : loser_lst
    }
        
def distribute_point():
    yesterday = date.today() - timedelta(days=1)
    challenges = Challenge.objects.filter(finish_at = yesterday).all()
    log = []
    for c in challenges:
        data = calc_point(c)
        log.append(data)
    print(log)
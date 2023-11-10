from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'challenges'

router = DefaultRouter()
router.register(r'', ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('list/<str:state>/', ChallengeList.as_view()),
    path('detail/<int:challenge_id>/', ChallengeInfo.as_view()),
    path('', include(router.urls)),
    path('certify/<int:challenge_id>/', CreateCertify.as_view()),
    path('certify/list/<int:challenge_id>/', CertifyList.as_view()),
    path('certify/list/detail/<int:challenge_id>/', ChallengersInfoList.as_view()),
    path('certify/my/<int:challenge_id>/', MyCertifies.as_view()),
    path('participate/<int:challenge_id>/', ParticipateChallenge.as_view()),
]
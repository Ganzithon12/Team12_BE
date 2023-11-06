from django.urls import path
from .views import *

app_name = 'challenges'

urlpatterns = [
    path('create/', CreateChallenge.as_view()),
    path('certify/<int:challenge_id>/', CreateCertify.as_view()),
    path('participate/<int:challenge_id>/', ParticipateChallenge.as_view()),
]
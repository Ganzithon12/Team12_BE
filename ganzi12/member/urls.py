from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'member'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('info/', user_info),
    path('rank/', RankView.as_view()),
]
from django.urls import path
from .views import *

app_name = 'member'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', login),
    path('logout/', logout),
]
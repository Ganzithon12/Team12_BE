from django.contrib import admin
from .models import Challenge, ChallengeCompleted

admin.site.register(Challenge)
admin.site.register(ChallengeCompleted)
from django.db import models
from ..member.models import *

# Create your models here.
class Challenge(models.Model):
    title = models.CharField(max_length=128)
    entry_fee = models.IntegerField(null = False)
    start_at = models.DateField(auto_now = False, auto_now_add = False)
    finish_at = models.DateField(auto_now = False, auto_now_add = False)
    period = models.IntegerField(null = False)
    challengers = models.ManyToManyField(CustomUser, related_name="challengers", null = True)
    challenge_logo = models.ImageField(blank = True, null = True, upload_to='challenge_image')

    def __str__(self):
        return self.title
from django.db import models
from member.models import *


class Challenge(models.Model):
    title = models.CharField(max_length=128)
    entry_fee = models.IntegerField(null = False)
    start_at = models.DateField(auto_now = False, auto_now_add = False)
    finish_at = models.DateField(auto_now = False, auto_now_add = False)
    period = models.IntegerField(default = 0)
    challengers = models.ManyToManyField(CustomUser, related_name="challengers", null = True)
    challenge_logo = models.ImageField(blank = True, null = True, upload_to='challenge_image')
    maximum_num = models.IntegerField(null = False)
    current_num = models.IntegerField(default=0)
    sum_point = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        days = self.finish_at - self.start_at
        self.period = days.days + 1
        super(Challenge, self).save(*args, **kwargs)
    
class ChallengeCompleted(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    challenge_image = models.ImageField(blank = False, upload_to=f"challenges/{challenge}")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.writer} - {self.challenge} ({self.created_at})"
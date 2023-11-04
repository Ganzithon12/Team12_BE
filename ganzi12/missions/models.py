from django.db import models
from member.models import CustomUser
from django.utils import timezone


class Mission(models.Model):
    mission_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    point = models.PositiveIntegerField(default=0)
    mission_logo = models.ImageField(verbose_name='mission', blank=True, null=True, upload_to='mission_image')

    def __str__(self):
        return self.title

class MissionCompleted(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mission_image = models.ImageField(verbose_name='missionCompleted', blank=False)
    status = models.BooleanField(default=False)
    completion_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.completion_date:
            self.completion_date = timezone.now().date()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.writer} - {self.mission} ({self.completion_date.strftime('%Y%m%d')})"
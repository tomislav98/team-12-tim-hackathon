from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import datetime
from Hackathon_app.submodels.iot_models import *
# Create your models here.

class ReportMap(models.Model):
    id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=2000)
    Name = models.CharField(max_length=2000)
    Description = models.CharField(max_length=2000)
    Icon = models.ForeignKey(KindIconFeature, on_delete=models.CASCADE)
    LongitudePosition = models.FloatField(max_length=2000, null=False)
    LatitudePosition = models.FloatField(max_length=2000, null=False)

class Role(models.Model):
  STANDARD_USER = 1
  ROLE_CHOICES = [
      (STANDARD_USER, 'Utente standard')
  ]

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()

class KindAction(models.Model):
    id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=2000)
    Name = models.CharField(max_length=2000)
    Description = models.CharField(max_length=2000)
    Score = models.FloatField(null=False)
    StartDateValidation = models.DateTimeField(null=False, auto_created=True)
    EndDateValidation = models.DateTimeField(null=True)
    Enabled =  models.BooleanField(null=False, default=True)
    Content = models.TextField()
    BinDevice = models.ForeignKey(BinDevice, on_delete=models.CASCADE, null=True, blank=True)
    Report = models.ForeignKey(ReportMap, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.Name} - {self.Description}'


class KindMission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=2000)
    DisplayName = models.CharField(max_length=2000)
    Description = models.CharField(max_length=2000)
    StartDateValidation = models.DateTimeField(null=False, auto_created=True)
    EndDateValidation = models.DateTimeField(null=True)
    Score = models.FloatField()
    KindActions = models.ManyToManyField(KindAction)

class User(AbstractUser):
  roles = models.ManyToManyField(Role, blank=True)
  Missions = models.ManyToManyField(KindMission)

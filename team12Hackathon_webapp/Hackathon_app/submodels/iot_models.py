from django.db import models
from datetime import datetime

class KindIconFeature(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=False)
    DisplayName = models.CharField(max_length=200)
    Description = models.CharField(max_length=2000)
    Base64 = models.BinaryField(max_length=9999)


class KindGenericDevice(models.Model):

    Id = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=2000,null=True)
    SerialNo = models.CharField(max_length=2000,null=False)
    ModelNo =  models.CharField(max_length=2000,null=False)
    Brand = models.CharField(max_length=2000,null=False)
    Code = models.CharField(max_length=2000,null=False)

class BinDevice(KindGenericDevice):

    MacAddress = models.CharField(max_length=2000,null=False)
    LongitudePosition = models.FloatField(max_length=2000,null=False)
    LatitudePosition = models.FloatField(max_length=2000, null=False)
    Zone = models.CharField(max_length=2000,null=False)
    LastUpdate = models.DateTimeField(auto_created=True)
    Icon = models.ForeignKey(KindIconFeature, on_delete=models.CASCADE)

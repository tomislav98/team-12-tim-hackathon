from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

class Role(models.Model):
  STANDARD_USER = 1
  ROLE_CHOICES = [
      (STANDARD_USER, 'Utente standard')
  ]

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()

class User(AbstractUser):
  roles = models.ManyToManyField(Role)

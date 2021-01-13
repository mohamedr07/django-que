from django.db import models
from users.models import User

# Create your models here.
class ServiceStation(models.Model):
    name=models.CharField(max_length=150)
    provider = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
from django.db import models

# Create your models here.
from django.db import models
from queues.models import Queue 
from users.models import User
# Create your models here.
class Process(models.Model):
    name=models.CharField(max_length=150)
    queues=models.ManyToManyField(Queue)

class Process_User(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    process=models.ForeignKey(Process,on_delete=models.CASCADE)
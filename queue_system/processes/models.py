from django.db import models
from queues.models import Queue 
from users.models import User

class Process(models.Model):
    name=models.CharField(max_length=150)
    queues=models.ManyToManyField(Queue)

class Process_User(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    process = models.ForeignKey(Process,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)  

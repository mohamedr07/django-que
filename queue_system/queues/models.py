from django.db import models
from users.models import User
import processes.models

class Queue(models.Model):
    name=models.CharField(max_length=150)
    estimated_time=models.IntegerField()
    
    def __str__(self):
        return self.name

class User_Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    booking = models.ForeignKey("processes.Process_User", on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    joined_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

class Live_Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
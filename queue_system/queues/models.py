from django.db import models
from users.models import User
# Create your models here.
class Queue(models.Model):
    name=models.CharField(max_length=150)
    estimated_time=models.IntegerField()
    users=models.ManyToManyField(User)

    def __str__(self):
        return self.name

class User_Queue(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    queue=models.ForeignKey(Queue,on_delete=models.CASCADE)
from django.db import models

# Create your models here.
from django.db import models
from queues.models import Queue 
# Create your models here.
class Process(models.Model):
    name=models.CharField(max_length=150)
    queues=models.ManyToManyField(Queue)

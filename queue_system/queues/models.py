from django.db import models

# Create your models here.
class Queue(models.Model):
    name=models.CharField(max_length=150)
    estimated_time=models.IntegerField()

    def __str__(self):
        return self.name
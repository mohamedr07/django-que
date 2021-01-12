from rest_framework import serializers
from queues.models import Queue,User_Queue

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Queue
        fields='__all__'
class CreateQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Queue
        fields=['name','estimated_time']
class UserQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Queue
        fields='__all__'
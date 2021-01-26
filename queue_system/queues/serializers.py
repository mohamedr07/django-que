from rest_framework import serializers
from queues.models import Queue,User_Queue,Live_Queue

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

class LiveQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Live_Queue
        fields='__all__'
    
    def checkAvailable(self):
        if Live_Queue.objects.filter(user_id = self.validated_data['user']).filter(queue_id = self.validated_data['queue']).exists():
            return False
        return True
        
    
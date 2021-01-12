from rest_framework import serializers
from processes.models import Process
from queues.serializers import QueueSerializer

class ProcessSerializer(serializers.ModelSerializer):
    queues =QueueSerializer(many=True)
    class Meta:
        model=Process
        fields='__all__'
class CreateProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model=Process
        fields='__all__'
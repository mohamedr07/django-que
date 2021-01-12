from rest_framework import serializers
from processes.models import Process,Process_User
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


class ProcessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Process_User
        fields=['process']
class CreateProcessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Process_User
        fields='__all__'

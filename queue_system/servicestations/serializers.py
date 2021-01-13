from rest_framework import serializers
from .models import ServiceStation
from users.serializers import UserSerializer

class StationSerializer(serializers.ModelSerializer):
    provider = UserSerializer()
    class Meta:
        model=ServiceStation
        fields='__all__'

class CreateStationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceStation
        fields=['name']
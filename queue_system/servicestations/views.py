from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ServiceStation
from .serializers import StationSerializer,CreateStationSerializer
from users.models import User
# Create your views here.

@api_view(['GET','POST'])
def stations_list(request):
    if request.method == 'GET':
        stations = StationSerializer(ServiceStation.objects.all(),many=True)
        return Response(stations.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CreateStationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','PUT','DELETE'])
def station(request,pk):
    if request.method == 'GET':
        station = StationSerializer(ServiceStation.objects.get(id=pk))
        return Response(station.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        station = ServiceStation.objects.get(id=pk)
        serializer = CreateStationSerializer(data=request.data)
        provider = User.objects.get(id=request.data['provider'])
        if serializer.is_valid():
            station.name=request.data['name']
            station.provider=provider
            station.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        station = ServiceStation.objects.get(id=pk)
        station.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Process
from .serializers import ProcessSerializer,CreateProcessSerializer
# Create your views here.
@api_view(['GET','POST'])
def processes_list(request):
    if request.method == 'GET':
        services = Process.objects.all()
        serializer = ProcessSerializer(services,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CreateProcessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def process(request,pk):
    if request.method == 'GET':
        service = Process.objects.get(id=pk)
        serializer = ProcessSerializer(service)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        service = Process.objects.get(id=pk)
        serializer = CreateProcessSerializer(data=request.data)
        if serializer.is_valid():
            service.name=request.data['name']
            service.queues.set(request.data['queues'])
            service.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        service = Process.objects.get(id=pk)
        service.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

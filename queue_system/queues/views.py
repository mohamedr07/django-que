from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Queue
from .serializers import QueueSerializer,CreateQueueSerializer

# Create your views here.

@api_view(['GET','POST'])
def queues_list(request):
    if request.method == 'GET':
        queues = Queue.objects.all()
        serializer = QueueSerializer(queues,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CreateQueueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def queue(request,pk):
    if request.method == 'GET':
        queue = Queue.objects.get(id=pk)
        serializer = QueueSerializer(queue)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        queue = Queue.objects.get(id=pk)
        serializer = CreateQueueSerializer(data=request.data)
        if serializer.is_valid():
            queue.name=request.data['name']
            queue.estimated_time=request.data['estimated_time']
            queue.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        queue = Queue.objects.get(id=pk)
        queue.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Queue
from .serializers import QueueSerializer,CreateQueueSerializer
from .models import User_Queue


# Create your views here.

@api_view(['GET','POST'])
def queues_list(request):
    if request.method == 'GET':
        queues = Queue.objects.all().order_by('id')
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
        serializer = CreateQueueSerializer(instance=queue,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        queue = Queue.objects.get(id=pk)
        queue.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def join_next_queue(request):
    if request.method == 'POST':
        next_queue = User_Queue.objects.filter(user=request.data['user']).first().queue
        queue=Queue.objects.get(id=next_queue.id)
        queue.users.add(request.data['user'])
        return Response({'msg':'user joined queue successfully'},status=status.HTTP_200_OK)

@api_view(['PUT'])
def advance_queue(request,pk):
    if request.method == 'PUT':
        queue = Queue.objects.get(id=pk)
        serializer = QueueSerializer(queue)
        users=serializer.data['users']
        selected_user = users.pop(0)
        queue.users.set(users)
        queue.save()
        User_Queue.objects.filter(user=selected_user,queue=pk).delete()
        return Response({'user':selected_user},status=status.HTTP_200_OK)

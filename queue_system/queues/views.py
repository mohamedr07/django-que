from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Queue
from processes.models import Process_User
from .serializers import QueueSerializer,CreateQueueSerializer, UserQueueSerializer, LiveQueueSerializer
from processes.serializers import CreateProcessUserSerializer
from .models import User_Queue, Live_Queue
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
import datetime


@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def queues_list(request):
    if request.user.is_superuser == True:
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
    else:
        return Response('Access denied')

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAdminUser])
def queue(request,pk):
    if request.user.is_superuser == True:
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
    else:
        return Response('Access denied')

@api_view(['POST'])
def join_next_queue(request):
    if request.method == 'POST':
        next_queue = User_Queue.objects.filter(user=request.data['user']).first().queue
        queue=Queue.objects.get(id=next_queue.id)
        queue.users.add(request.data['user'])
        return Response({'msg':'user joined queue successfully','queue':next_queue.id},status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def advance_queue(request,pk):
    if request.method == 'PUT':
        queue = Live_Queue.objects.filter(queue_id = pk).first()
        uq = User_Queue.objects.filter(completed= False).filter(user = queue.user_id).filter(queue = queue.queue_id).first()
        data = {
            'completed': True,
            'completed_at': datetime.datetime.now()
        }
        booking = uq.booking_id
        serializer = UserQueueSerializer(instance=uq,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
        data2 = User_Queue.objects.filter(completed= False).filter(user = queue.user_id).first()
        if not User_Queue.objects.filter(booking = booking).filter(completed = False).exists():
            processData = {
                'completed': True,
                'completed_at': datetime.datetime.now()
            }
            process = Process_User.objects.get(id=booking)
            serializer3 = CreateProcessUserSerializer(instance=process,data=processData,partial=True)
            if serializer3.is_valid():
                serializer3.save()
            else:
                pass
        queue.delete()
        serializer2 = LiveQueueSerializer(data = {'user': data2.user_id, 'queue': data2.queue_id})
        if serializer2.is_valid():
            serializer2.save()
        else:
            pass
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

        # queue = Queue.objects.get(id=pk)
        # serializer = QueueSerializer(queue)
        # users=serializer.data['users']
        # selected_user = users.pop(0)
        # queue.users.set(users)
        # queue.save()
        # User_Queue.objects.filter(user=selected_user,queue=pk).delete()
        # return Response({'user':selected_user},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user_info(request,pk):
    if request.method =='GET':
        queue = Queue.objects.get(id=pk)
        serializer = QueueSerializer(queue)
        users=serializer.data['users']
        position=users.index(request.data['user'])
        estimated_time=(position+1)*queue.estimated_time
        return Response({position,estimated_time},status=status.HTTP_200_OK)
        
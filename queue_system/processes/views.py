from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Process,Process_User
from .serializers import ProcessSerializer,CreateProcessSerializer,CreateProcessUserSerializer
from queues.models import User_Queue
from queues.serializers import UserQueueSerializer, LiveQueueSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
import datetime

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def processes_list(request):
    if request.method == 'GET':
        processes = Process.objects.all().order_by('id')
        serializer = ProcessSerializer(processes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if request.user.is_superuser == True:
            serializer = CreateProcessSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Access denied')    

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAdminUser])
def process(request,pk):
    if request.user.is_superuser == True:
        if request.method == 'GET':
            process = Process.objects.get(id=pk)
            serializer = ProcessSerializer(process)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            process = Process.objects.get(id=pk)
            serializer = CreateProcessSerializer(instance=process,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            process = Process.objects.get(id=pk)
            process.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response('Access denied')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_process(request,pk):
    if request.method == 'POST':
        process = Process.objects.get(id=pk)
        if not process:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {'user':request.data['user'],'process':pk}
        serializer = CreateProcessUserSerializer(data=data)
        if serializer.is_valid() and not Process_User.objects.filter(user_id = request.data['user']).filter(process_id = pk).filter(completed = False).exists():
            serializer.save()
            processSerializer = ProcessSerializer(process)
            queuesList=[q['id'] for q in processSerializer.data['queues']]
            booking = serializer.data['id']
            
            for queue in queuesList:
                if User_Queue.objects.filter(user_id = request.data['user']).filter(queue_id = queue).filter(booking = booking).exists():
                    pass
                else:
                    data={'user':request.data['user'], 'queue':queue, 'booking':booking, 'joined_at':datetime.datetime.now()}
                    serializer2 = UserQueueSerializer(data=data)
                    if serializer2.is_valid():
                        serializer2.save()
                    else:
                        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            queue3 = User_Queue.objects.filter(user_id = request.data['user'])[0].queue_id
            user3 = request.data['user']
            data3 = {'user': user3, 'queue': queue3}
            serializer3 = LiveQueueSerializer(data = data3)
            if(serializer3).is_valid():
                if serializer3.checkAvailable():
                    serializer3.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Access denied')

        
        

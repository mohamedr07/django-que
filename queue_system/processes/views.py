from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Process,Process_User
from .serializers import ProcessSerializer,CreateProcessSerializer,CreateProcessUserSerializer
from queues.models import User_Queue
from queues.serializers import UserQueueSerializer

# Create your views here.
@api_view(['GET','POST'])
def processes_list(request):
    if request.method == 'GET':
        processes = Process.objects.all().order_by('id')
        serializer = ProcessSerializer(processes,many=True)
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

@api_view(['POST'])
def join_process(request,pk):
    if request.method == 'POST':
        process = Process.objects.get(id=pk)
        if not process:
            return Response(status=status.HTTP_404_NOT_FOUND)
        processSerializer = ProcessSerializer(process)
        queuesList=[q['id'] for q in processSerializer.data['queues']]
        print(queuesList)
        for queue in queuesList:
            data={'user':request.data['user'],'queue':queue}
            serializer = UserQueueSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data = {'user':request.data['user'],'process':pk}
        serializer = CreateProcessUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

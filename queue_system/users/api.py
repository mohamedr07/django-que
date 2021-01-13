from users.models import User 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from processes.models import Process_User
from processes.serializers import ProcessUserSerializer
from queues.models import User_Queue
from queues.serializers import UserQueueSerializer


@api_view(['GET',])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def user(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id = pk)
        serializer = UserSerializer(user, many = False)
        processesSerializer=ProcessUserSerializer(Process_User.objects.filter(user=pk),many=True)
        processesList=[p['process'] for p in processesSerializer.data]
        processes={'processes':processesList}
        queuesSerializer = UserQueueSerializer(User_Queue.objects.filter(user=pk),many=True)
        queuesList=[q['queue'] for q in queuesSerializer.data]
        queues={'queues':queuesList}
        data={**serializer.data,**processes,**queues}
        return Response({'user':data})
    elif request.method == 'PUT':
        user = User.objects.get(id = pk)
        serializer = UserSerializer(instance = user, data = request.data, partial = True)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully updated a new user."
            data['id'] = user.id
            data['full_name'] = user.full_name
            data['email'] = user.email
        else:
            data = serializer.errors
        return Response(data)
    elif request.method == 'DELETE':
        user = User.objects.get(id = pk)
        user.delete()
        return Response('User deleted successfully')

@api_view(['POST',])
def register_user(request):

    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.reg_user()
            data['response'] = "successfully registered a new user."
            data['id'] = user.id
            data['full_name'] = user.full_name
            data['email'] = user.email
        else:
            data = serializer.errors
        return Response(data)





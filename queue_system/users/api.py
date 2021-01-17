from users.models import User 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import UserSerializer
from processes.models import Process_User
from processes.serializers import ProcessUserSerializer
from queues.models import User_Queue
from queues.serializers import UserQueueSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET',])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.reg_user()
            return Response("Registered successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@permission_classes([AllowAny])
def blacklistToken(request):
    if request.method == 'POST':
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Successfully logged out")
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_providers(request):
    if request.method == 'GET':
        users = User.objects.filter(is_staff=True)
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)


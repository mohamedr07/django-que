from users.models import User 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer


@api_view(['GET',])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

@api_view(['GET',])
def user(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id = pk)
        serializer = UserSerializer(user, many = False)
        return Response(serializer.data)

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

@api_view(['PUT',])
def update_user(request, pk):

    if request.method == 'PUT':
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


@api_view(['DELETE',])
def delete_user(request, pk):

    if request.method == 'DELETE':
        user = User.objects.get(id = pk)
        user.delete()
        return Response('User deleted successfully')

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = UserSerializer

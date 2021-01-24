from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        data['id'] = self.user.id
        return data

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'full_name': {'required': True}
        } 
    
    def reg_user(self):
        user = User(
            email = self.validated_data['email'],
            full_name = self.validated_data['full_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords must match.'})
        user.set_password(password)
        user.save()
        return user
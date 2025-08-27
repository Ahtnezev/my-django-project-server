from rest_framework import serializers
from .models import User
import bcrypt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User #user model from models.py
        fields = ['id', 'name', 'lastname', 'email', 'phone', 'image', 'password', 'notification_token']
        extra_kwargs = { #do not show password in response
            'password': {'write_only': True}
        }

    # with validated_data only
    # {
    #     'name': 'vicente',
    #     'field_x': 'value_x'
    # }
    # with ** added
    # name = 'vicente'
    def create(self, validated_data):
        raw_password = validated_data.pop('password') #encrypt password
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')
        user = User.objects.create(**validated_data)
        return user


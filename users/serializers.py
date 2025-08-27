from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User #user model from models.py
        fields = ['id', 'name', 'lastname', 'email', 'phone', 'image', 'password', 'notification_token']

    # with validated_data only
    # {
    #     'name': 'vicente',
    #     'field_x': 'value_x'
    # }
    # with ** added
    # name = 'vicente'
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


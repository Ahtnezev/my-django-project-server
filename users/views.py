from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from users.serializers import UserSerializer

# create a custom python environment -> venv
# display IP: ipconfig getifaddr <en0, en1>
# create a virtual environment: python3.11 -m venv <venv>
# active venv: source <venv>/bin/activate
# exit: (venv...) deactivate

# (venv) pip list
# django, djangorestframework, pymysql

# Create your views here.
# GET, POST, PUT, DELETE

@api_view(['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(): # Validate the data
        serializer.save() # Save in database
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import get_object_or_404, render

import bcrypt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from roles.models import Role
from roles.serializers import RoleSerializer
from users.models import User, UserHasRoles
from users.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings

# create a virtual environment: python3.11 -m venv <venv>
# active venv: source <venv>/bin/activate
# exit: (venv...) deactivate
# pip freeze > requirements.txt
# (another venv) pip install -r requirements.txt

# (venv) pip list
# django, djangorestframework, pymysql

# create a new module with: python manage.py startapp <app_name> -> authentication
# auth no 'cause it's exists

# create new module: ... startapp roles

# Create your views here.
# GET, POST, PUT, DELETE
# 4	Yunnuee	Martinez	yun@mart.com	3331487432
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(): # Validate the data
        user = serializer.save()

        client_role = get_object_or_404(Role, id="CLIENT")
        UserHasRoles.objects.create(id_user=user, id_rol=client_role)
        roles = Role.objects.filter(userhasroles__id_user=user)
        roles_serializer = RoleSerializer(roles, many=True) # many to indicate that is a list
        response_data = {
            **serializer.data,
            "roles": roles_serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    error_messages = []
    for field, errors in serializer.errors.items():
        for error in errors:
            error_messages.append(f"{field}: {error}")
    
    # dict, format to error response in postman
    error_response = {
        "message": error_messages,
        "statusCode": status.HTTP_400_BAD_REQUEST
    }

    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)



# this info comes after paste our jwt in jwt.io and get the user_id field. The
# database doesnt recognize the user_id field, so we need to add it manually and replace by id field
def getCustomTokenForUser(user):
    refresh_token = RefreshToken.for_user(user)
    del refresh_token.payload['user_id']
    refresh_token.payload['id'] = user.id
    refresh_token.payload['name'] = user.name
    return refresh_token

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {
                "message": "El email y password son obligatorios",
                "statusCode": status.HTTP_400_BAD_REQUEST
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"message": "El email o password no son correctos", "statusCode" : status.HTTP_401_UNAUTHORIZED},
            status=status.HTTP_401_UNAUTHORIZED
        )
        
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        refresh_token = getCustomTokenForUser(user)
        access_token = str(refresh_token.access_token)
        roles = Role.objects.filter(userhasroles__id_user=user)
        roles_serializer = RoleSerializer(roles, many=True)
        user_data = {
            "user": {
                "id": user.id,
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "phone": user.phone,
                "image": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{user.image}' if user.image else None,
                "notification_token": user.notification_token,
                "roles": roles_serializer.data,
            },
            "token": "Bearer " + access_token
        }
        return Response(user_data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "El email o password no son correctos", "statusCode" : status.HTTP_401_UNAUTHORIZED},
            status=status.HTTP_401_UNAUTHORIZED
        )
from django.urls import path
from .views import register, login

# http://127.0.0.1:8000/api/users on postman
# http://127.0.0.1:8000/users on postman (new)

urlpatterns = [
    path('register', register),
    path('login', login)
]
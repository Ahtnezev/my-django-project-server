from django.urls import path
from .views import update

urlpatterns = [
    path('/<id_user>', update),
    # path('/login', login)
]
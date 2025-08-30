from django.urls import path
from .views import update, updateWithImage, get_user_by_id, get_all_users

urlpatterns = [
    path('/<id_user>', update), # PUT
    path('/findById/<id_user>', get_user_by_id), # GET
    path('/upload/<id_user>', updateWithImage), # PUT
    path('/', get_all_users), #GET
]
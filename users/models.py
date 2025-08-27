from django.db import models

# command to execute: python3 manage.py makemigrations 
# python3 manage.py migrate

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    image = models.CharField(max_length=255, null=True, blank=False) #blank: empty string not allowed
    password = models.CharField(max_length=255)
    notification_token = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # change table name (by default its <app_label<folder>>_<model_name>)
    # execute: python3 manage.py makemigrations
    # python3 manage.py migrate
    class Meta:
        db_table = 'users'
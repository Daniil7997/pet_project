from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserList(models.Model):
    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField()
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # (True/False) право на авторизацию.
#    permissions = models.CharField() права и ограничения


    # def get_absolute_url(self):
    #     return f'/post/{self.slug}/'


# https://www.geeksforgeeks.org/python/imagefield-django-models/

    def __str__(self):
        return self.email

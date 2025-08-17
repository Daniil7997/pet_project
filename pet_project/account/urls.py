from django.contrib import admin
from django.urls import path

from account.views import *


urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', login_user, name='login'),
    path('logout', logout_user, name='logout'),
]

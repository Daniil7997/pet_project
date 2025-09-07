from django.urls import path

from .views import *


urlpatterns = [
    path('', new_member),
]

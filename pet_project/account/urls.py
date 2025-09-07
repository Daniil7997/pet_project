from django.contrib import admin
from django.urls import path

from django.conf import settings  # -------
from django.conf.urls.static import static  # ---------

from account.views import *


urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile_settings/', profile_settings, name='profile_change'),
]

# для DEBUG = True
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

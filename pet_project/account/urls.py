from django.contrib import admin
from django.urls import path

from account.views import CreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CreateView.as_view()),
]
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from account.forms import *


class RegisterUser(CreateView):
    form_class = UserRegistrationForm  # UserCreationForm - функция джанго.
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


# https://www.youtube.com/watch?v=nfYlY5jEYPo


def login_user(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user=user)
            return redirect('login')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    redirect('login')

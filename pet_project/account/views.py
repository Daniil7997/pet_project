from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from account.forms import *


class RegisterUser(CreateView):
    form_class = RegisterUserForm  # UserCreationForm - функция джанго.
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


# https://www.youtube.com/watch?v=nfYlY5jEYPo


def login_user(request):
    form = LoginUserForm()
    if request.POST:
        form = LoginUserForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user=user)
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'login.html', context=context)


def logout_user(request):
    logout(request)
    redirect('login')

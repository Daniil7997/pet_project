from datetime import date

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Profile, UserAuth
from account.permissions import IsOwnerOrReadOnly
from account.serializers import ProfileSerializer
from account.forms import (
    RegisterUserForm,
    LoginUserForm,
    ProfileData,
)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        form_cd = form.cleaned_data
        try:
            self.registration_db_insert(data=form_cd)
        except Exception:
            form.add_error(None, "Ошибка при регистрации")
            return self.form_invalid(form)
        return HttpResponseRedirect(self.success_url)

    @transaction.atomic
    def registration_db_insert(self, data):
        data['password'] = make_password(data['password'])
        user = UserAuth.objects.create(
            password=data['password'],
            email=data['email']
        )
        user_profile = Profile.objects.create(
            name=data['name'],
            birthday=data['birthday'],
            sex=data['sex'],
            i_search=data['i_search'],
            auth_id=user.id,
        )
        return user_profile


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user=user)
            return redirect('home')
    else:
        form = LoginUserForm()
    context = {
        'form': form,
        'title': 'Вход',
    }
    return render(request, 'login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


def my_profile(request):
    user = Profile.objects.get(auth__email=request.user.email)
    dif_age = date.today() - user.birthday
    user.age = int(dif_age.days / 365)
    if request.method == 'POST':
        form = ProfileData(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('my_profile')
    else:
        form = ProfileData(instance=user)
    context = {'form': form, 'user': user}
    return render(request, 'my_profile.html', context=context)


@api_view(['GET'])
def user_list():
    tmp = Profile.objects.all()
    serializer = ProfileSerializer(tmp, many=True)
    return Response(serializer.data)


class CreateUser(CreateAPIView):
    serializer_class = ProfileSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
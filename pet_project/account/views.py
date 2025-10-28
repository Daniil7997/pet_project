from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db import transaction
from datetime import date

from account.models import Profile, UserAuth
from account.forms import (
    RegisterUserForm,
    LoginUserForm,
    ProfileData,
)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form_cd = form.cleaned_data
        self.db_insert(form_cd)
        return HttpResponseRedirect(self.success_url)

    @transaction.atomic
    def db_insert(self, form_cd):
        UserAuth.objects.create(
            password=form_cd['password'],
            email=form_cd['email']
        )
        user = UserAuth.objects.get(email=form_cd['email'])
        user_id = user.id
        print(f'{user_id} <----- USER_ID')
        Profile.objects.create(
            name=form_cd['name'],
            birthday=form_cd['birthday'],
            sex=form_cd['sex'],
            i_search=form_cd['i_search'],
            auth_id=user_id,
        )


def login_user(request):
    if request.POST:
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
    }
    return render(request, 'login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


def profile_edit(request):
    user = request.user
    Profile.objects.get(auth=user)


def my_profile(request):
    user = Profile.objects.get(auth__email=request.user.email)
    dif_age = date.today() - user.birthday
    user.age = int(dif_age.days / 365)
    if request.POST:
        form = ProfileData(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('my_profile')
    else:
        form = ProfileData(instance=user)

    context = {'form': form, 'user': user}
    return render(request, 'my_profile.html', context=context)




    # people = Person.objects.annotate(
    #     age=Func(
    #         ExtractYear(F('birth_date')),
    #         ExtractMonth(F('birth_date')),
    #         ExtractDay(F('birth_date')),
    #         Value(today.year),
    #         Value(today.month),
    #         Value(today.day),
    #         function='AGE',
    #         output_field=IntegerField()
    #     )
    # ) функция для вычисления возраста через бд для большого количества людей
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db import transaction

from account.forms import RegisterUserForm, LoginUserForm
from account.models import Profile, UserAuth


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
        Profile.objects.create(
            name=form_cd['name'],
            birthday=form_cd['birthday'],
            sex=form_cd['sex'],
            i_search=form_cd['i_search'],
            auth_id=user_id,
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        for key, value in kwargs.items():
            print(f'{key} <-- key\n{value} <-- value')
            context_data[key] = value
        return context_data

# https://www.youtube.com/watch?v=nfYlY5jEYPo authenticate, login, logout.


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


def profile_settings(request):
    pass

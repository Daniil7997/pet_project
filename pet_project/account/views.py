from django.http import HttpResponseRedirect
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

    def form_valid(self, form):
        # print(f'{form} {type(form)}')
        form_cd = form.cleaned_data
        form.save()
        self.profile_data(form_cd)

        return HttpResponseRedirect(self.success_url)

    @staticmethod
    def profile_data(form_cd):
        user = UserAuth.objects.get(email=form_cd['email'])
        user_id = user.id
        print(f'{user_id} <-- user\n{type(user_id)} <-- type(user)')
        Profile.objects.create(
            name=form_cd['name'],
            birthday=form_cd['birthday'],
            sex=form_cd['sex'],
            i_search=form_cd['i_search'],
            auth_id=user_id,
        )


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

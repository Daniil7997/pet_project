"""
https://pocoz.gitbooks.io/django-v-primerah/content/glava-4-sozdanie-social-website/reistratsiya-polzovatelei-i-profili-polzovatelei/registratsiya-polzovatelei.html
https://pocoz.gitbooks.io/django-v-primerah/content/glava-4-sozdanie-social-website/registratsiya-polzovatelei-i-profili-polzovatelei/registratsiya-polzovatelei.html
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django import forms

from .models import UserList

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = UserList  # - модель которая работает с таблицей auth_user в БД
        fields = ('email', 'password', 'password2')
        labels = {
            'password': 'Пароль',
            'password2': 'Повторите пароль',
            'email': 'Электронная почта',
        }
        help_texts = {
            'username': None,
        }

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        cd['password'] = make_password(cd['password'])
        return cd['password']

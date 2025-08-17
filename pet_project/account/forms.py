"""
https://pocoz.gitbooks.io/django-v-primerah/content/glava-4-sozdanie-social-website/reistratsiya-polzovatelei-i-profili-polzovatelei/registratsiya-polzovatelei.html
https://pocoz.gitbooks.io/django-v-primerah/content/glava-4-sozdanie-social-website/registratsiya-polzovatelei-i-profili-polzovatelei/registratsiya-polzovatelei.html
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django import forms

from .models import UserList


from django.contrib.auth.models import AbstractUser

class Test(UserCreationForm):
    pass


class RegisterUserForm(forms.ModelForm):

    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = UserList
        fields = ('email', 'password')
        labels = {
            'password': 'Пароль',
            'email': 'Электронная почта',
        }
        widgets = {
            'password': forms.PasswordInput,
            'password2': forms.PasswordInput,
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        cd['password'] = self.hash_password(cd['password'])
        return cd['password']

    @staticmethod
    def hash_password(raw_password):
        return make_password(raw_password)


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = UserList
        fields = ('email', 'password')
        labels = {
            'password': 'Пароль',
            'email': 'Электронная почта',
        }
        widgets = {
            'password': forms.PasswordInput,
        }

    # email = forms.EmailField(label='Электронная почта')
    # password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

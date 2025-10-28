from datetime import date

from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.hashers import make_password
from captcha.fields import CaptchaField, CaptchaTextInput

from .models import Profile


class RegisterUserForm(forms.ModelForm):

    # -- данные для модели Profile приложения account

    sex_choice = {'M': 'Мужской', 'W': 'Женский'}
    i_search_choice = {'M': 'Парня', 'W': 'Девушку'}

    sex = forms.ChoiceField(label='Пол', choices=sex_choice, widget=forms.RadioSelect)
    i_search = forms.ChoiceField(label='Я ищу', choices=i_search_choice, widget=forms.RadioSelect)
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    name = forms.CharField(label='Имя')

    # -- поле для подтверждения пароля
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    captcha_field = CaptchaField(widget=CaptchaTextInput(attrs={'placeholder': 'Введите код'}))

    class Meta:
        model = get_user_model()  # запрашивает AUTH_USER_MODEL из settings.py (UserAuth)
        fields = ('email', 'password')
        labels = {
            'password': 'Пароль',
            'email': 'Электронная почта',
        }
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_isearch(self):
        cd = self.cleaned_data
        if 'isearch' not in cd:
            raise forms.ValidationError('Выберите кого вы хотите найти.')
        return cd['isearch']

    def clean_password2(self):
        cd = self.cleaned_data
        if 'password2' not in cd:
            raise forms.ValidationError('Введите пароль')

        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        # хеширование пароля
        cd['password'] = make_password(cd['password'])
        return cd['password']

    def clean_sex(self):
        cd = self.cleaned_data
        if 'sex' not in cd:
            raise forms.ValidationError('Выберите пол.')
        return cd['sex']

    def clean_birthday(self):
        cd = self.cleaned_data
        if 'birthday' not in cd:
            raise forms.ValidationError('Введите дату рождения.')

        birthday = self.cleaned_data['birthday']
        today = date.today()
        age = today - birthday
        age = age.days / 365
        if age < 18:
            raise forms.ValidationError('Вам еще нет 18. ')

        return birthday

    def clean_name(self):
        cd = self.cleaned_data
        if 'name' not in cd:
            raise forms.ValidationError('Введите фамилию.')
        return cd['name']


class LoginUserForm(forms.ModelForm):
    captcha_field = CaptchaField(widget=CaptchaTextInput(attrs={'placeholder': 'Введите код'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        labels = {
            'password': 'Пароль',
            'email': 'Электронная почта',
        }
        widgets = {
            'password': forms.PasswordInput,
        }


class ProfileData(forms.ModelForm):
    sex_choice = {'M': 'Мужской', 'W': 'Женский'}
    i_search_choice = {'M': 'Парня', 'W': 'Девушку'}

    sex = forms.ChoiceField(label='Пол', choices=sex_choice, widget=forms.RadioSelect)
    i_search = forms.ChoiceField(label='Я ищу', choices=i_search_choice, widget=forms.RadioSelect)
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    name = forms.CharField(label='Имя')

    class Meta:
        model = Profile
        fields = ('name', 'sex', 'i_search', 'birthday', 'about', 'profile_photo')
        widgets = {
            'about': forms.Textarea,
        }

from datetime import date

from django.contrib.auth import get_user_model
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput

from .models import Profile, UserAuth


class RegisterUserForm(forms.ModelForm):
    sex_choice = {'M': 'Мужской', 'W': 'Женский'}
    i_search_choice = {'M': 'Парня', 'W': 'Девушку'}

    sex = forms.ChoiceField(label='Пол', choices=sex_choice, widget=forms.RadioSelect)
    i_search = forms.ChoiceField(label='Я ищу', choices=i_search_choice, widget=forms.RadioSelect)
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    name = forms.CharField(label='Имя')
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

    def clean_email(self):
        cd = self.cleaned_data
        if UserAuth.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return cd['email']

    def clean_i_search(self):
        cd = self.cleaned_data
        if 'i_search' not in cd:
            raise forms.ValidationError('Выберите кого вы хотите найти.')
        return cd['i_search']

    def clean_password2(self):
        cd = self.cleaned_data
        if 'password2' not in cd:
            raise forms.ValidationError('Введите пароль')

        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
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
        dif_date = date.today() - birthday
        age = int(dif_date.days / 365)
        if age < 18:
            raise forms.ValidationError('Вам еще нет 18. ')
        return birthday

    def clean_name(self):
        cd = self.cleaned_data
        if 'name' not in cd:
            raise forms.ValidationError('Введите имя.')
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

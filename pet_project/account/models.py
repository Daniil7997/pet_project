from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserList(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=50)
    is_active = models.BooleanField(default=True)  # (True/False) право на авторизацию.

    # из AbstractBaseUser наследуются следующие поля :
    # password = models.CharField(_("password"), max_length=128)
    # last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class UserData(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    about = models.CharField(max_length=250, verbose_name='О себе')
    photos = models.ImageField()
    profile_photos = models.ImageField()
    slug = models.SlugField(max_length=50, unique=True)


    def get_absolute_url(self):
        pass
        # return f'/user_page/{self.slug}/'

    def get_photo_path(self):
        return f'{self.slug}/'



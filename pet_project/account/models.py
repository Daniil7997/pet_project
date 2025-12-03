from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class UserAuth(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=50)
    is_active = models.BooleanField(default=False)  # (True/False) право на авторизацию.
    created_at = models.DateField(auto_now_add=True)

    # из AbstractBaseUser наследуются следующие поля :
    # password = models.CharField(_("password"), max_length=128)
    # last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):

    def user_photo_path(self, instance, filename):
        print('вызов USER_PHOTO_PATH')
        return f"users/{instance.id}/photos/{filename}"

    id = models.BigAutoField(primary_key=True)
    sex = models.CharField(verbose_name='Пол')
    name = models.CharField(max_length=20, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')
    about = models.CharField(max_length=250, blank=True, verbose_name='О себе')
    profile_photo = models.ImageField(blank=True, default='', verbose_name='Фото профиля', upload_to=user_photo_path)
    i_search = models.CharField(verbose_name='Я ищу')
    auth = models.OneToOneField(UserAuth, on_delete=models.CASCADE, related_name='profile', unique=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/user_page/{self.id}/'

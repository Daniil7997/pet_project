from django.db import models


class UserList(models.Model):
    f_name = models.CharField(max_length=50, verbose_name='Имя')
    l_name = models.CharField(max_length=50, verbose_name='Фамилия')
    slug = models.SlugField(max_length=50, unique=True, blank=False, null=False, verbose_name='URL')
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name='Время регистрации')

    def __str__(self):
        return f'{str(self.f_name)} {str(self.l_name)}'

    def get_absolute_url(self):
        return f'/post/{self.slug}/'


# https://www.geeksforgeeks.org/python/imagefield-django-models/
def path_to_user_directory(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserData(models.Model):

    about_myself = models.CharField(max_length=500, verbose_name='О себе')
    photo = models.ImageField(upload_to=path_to_user_directory, verbose_name='Фото')

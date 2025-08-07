from django.db import models

from account.models import UserList


class UserData(models.Model):
    sex_choices = [['М', 'Мужской'],
                   ['Ж', 'Женский']]

    sex_search = [['М', 'Парня'],
                  ['Ж', 'Девушку']]

    f_name = models.CharField(max_length=50, verbose_name='Имя')
    l_name = models.CharField(max_length=50, verbose_name='Фамилия')
    sex = models.CharField(choices=sex_choices)
    about_me = models.TextField(max_length=250, blank=True, verbose_name='о себе')
    search = models.CharField(choices=sex_search)
    relationship_goal = models.CharField(max_length=250, verbose_name='Цель отношений')
    slug = models.SlugField(unique=True)
    UserID = models.OneToOneField(
        UserList,
        on_delete=models.CASCADE,
    )

    # def path_to_user_directory(instance, filename):
    #     # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    #     return 'user_{0}/{1}'.format(instance.user.id, filename)

    def __str__(self):
        return f'{str(self.f_name)} {str(self.l_name)}'

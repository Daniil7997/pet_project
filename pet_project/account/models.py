from django.db import models


class UserList(models.Model):
    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField()



    # def get_absolute_url(self):
    #     return f'/post/{self.slug}/'


# https://www.geeksforgeeks.org/python/imagefield-django-models/

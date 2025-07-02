from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import *


class RegisterUser(CreateView):
    form_class = UserRegistrationForm  # UserCreationForm - функция джанго.
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title='Регистрация')
    #     return {**context, **c_def}
# атрибут success_url отвечает за перенаправление на адрес после завершения работы класса представления
# (в данном случае после создания новой записи в таблице women)
# Т.е. произойдёт перенаправление на url имеющий имя 'home'
#
# функция reverse_lazy работает как и reverse с той лишь разницей, что
# reverse выполняет построение маршрута в момент создания экземпляра класса,
# reverse_lazy выполняет построение маршрута только когда маршрут понадобится

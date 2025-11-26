from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'base.html', context=context)

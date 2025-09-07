from django.shortcuts import render, redirect


# Create your views here.

def new_member(request):
    return redirect('login')

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def registrar(request):
    return render(request, 'Register/archive.html')
    
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    # return HttpResponse("Views")
    return render(request,"Register/index.html")

def greet(request, name):
    return render(request, 'hello/greet.html', {
        "name": name.title()
    })
    
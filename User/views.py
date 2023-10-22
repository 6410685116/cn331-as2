from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from Register import views

def login_view(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(views.registrar))
        else:
            return render(request, 'User/login.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, "User/login.html")
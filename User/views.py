from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from Register import views

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'registration/index.html')


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


def logout_view(request):
    logout(request)
    return render(request, 'registration/login.html', {
        'message': 'Logged out'
    })
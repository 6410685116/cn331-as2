from django.urls import path, include
from . import views

urlpatterns =[
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
    # path('', include("django.contrib.auth.urls")),
    
]
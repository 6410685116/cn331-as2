from django.urls import path, include
from . import views

urlpatterns =[
    path('index/', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout')
    # path('', include("django.contrib.auth.urls")),
    
]
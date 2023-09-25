from django.urls import path, include
from . import views

app_name = 'Register'

urlpatterns =[
    path('', views.index, name='index'),
    path('<str:name>', views.greet, name='greet'),
]
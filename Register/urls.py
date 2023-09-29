from django.urls import path, include
from . import views


urlpatterns =[
    path('registrar/', views.registrar, name='registrar'),
    path('quota/', views.quota, name='quota')
]
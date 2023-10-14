from django.urls import path, include
from . import views


urlpatterns =[
    path('registrar/', views.registrar, name='registrar'),
    path('quota/', views.quota, name='quota'),
    path('listquota/', views.quotalist, name='listquota'),
    path('add_student/<int:course_id>',views.add_student, name='add_student'),
    path('delete/<int:course_id>',views.delete, name ="delete"),
    path('logout/',views.logout_view, name ="logout"),
]
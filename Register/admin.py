from django.contrib import admin
from Register.models import Student
from .models import Subject
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Surname', 'Student_number']
    search_fields = ['Student_number', 'Name', 'Surname']
    list_filter = ['Student_number', 'Name', 'Surname']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id_course', 'course',  'Semester', 'Year', 'quota', 'max_quota', 'is_open', ]
    search_fields = ['course', 'Semester', 'Year']
    list_filter = ['is_open', 'Year', 'Semester']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)

from django.contrib import admin
from Register.models import Student
from .models import Subject
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Surname', 'Student_number']
    search_fields = ['Student_number', 'Name', 'Surname']
    list_filter = ['Student_number', 'Name', 'Surname']

def remove_student_from_course(queryset):
    for subject in queryset:
        subject.Subject.clear()

remove_student_from_course.short_description = "Remove selected students from courses"

class SubjectAdmin(admin.ModelAdmin):
    # list_display = ['course', 'Semester', 'Year', 'max_quota', 'is_open', 'quota']
    list_display = ['course', "id_course", 'Semester', 'Year', 'is_open', 'quota', ]
    search_fields = ['course', 'Semester', 'Year']
    list_filter = ['is_open', 'Year', 'Semester']
    actions = [remove_student_from_course]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)

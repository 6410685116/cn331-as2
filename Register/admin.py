from django.contrib import admin
from Register.models import Student
from .models import Subject
# Register your models here.

admin.site.register(Student)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['course', 'Semester', 'Year', 'max_quota', 'is_open', 'current_enrollment']
    search_fields = ['course', 'Semester', 'Year']
    list_filter = ['is_open', 'Year', 'Semester']

    def current_enrollment(self, obj):
        return obj.current_enrollment()

    current_enrollment.short_description = 'Enrollment Count'

admin.site.register(Subject, SubjectAdmin)

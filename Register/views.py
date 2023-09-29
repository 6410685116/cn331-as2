from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Subject, Student

# Create your views here.

def registrar(request):
    return render(request, 'Register/archive.html')


def subject(request, course_id):
    course = get_object_or_404(Subject, id=course_id)

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student, created = Student.objects.get_or_create(name=student_name)

        if not course.is_full() and student not in course.students.all():
            course.students.add(student)

    return render(request, 'enrollment/enroll.html', {'course': course})

def quota(request):
    all_quota = Subject.objects.all()
    return render(request, 'Register/quota.html',{"all_quota":all_quota})
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Student
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse


# Create your views here.

def registrar(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    return render(request, './Register/archive.html',{
        'student': student,
    })

def quota(request):
    user = request.user
    student = get_object_or_404(Student, user=user) 
    return render(request, './Register/quota.html',{
        "all_course": Subject.objects.exclude(students = student),
        'message': "กดลงวิชาไม่ได้เนื่องจากเต็ม",
        })

def add_student(request, course_id):
    user = request.user
    student = get_object_or_404(Student, user=user) 
    course = get_object_or_404(Subject, pk=course_id)

    if request.method == "POST":
        if 0 >= course.quota:
            return render(request, "./Register/quota.html", {
                'message': 'โค้วต้าเต็ม',
                'all_course': Subject.objects.all(),
            })
        else:
            course.students.add(student)
            course.quota -= 1
            course.save()
            return render(request, "./Register/quota.html", {
                'message': 'Success',
                'all_course': Subject.objects.exclude(students = student),
            })
    return HttpResponseRedirect(reverse('/'))

def quotalist(request):
    user = request.user
    student = Student.objects.get(user = user)
    enrolled_courses = Subject.objects.filter(students = student)
    return render(request, './Register/listquota.html', {
        "enrolled_courses": enrolled_courses,
        'user': user,
    })

def delete(request, course_id):
    user = request.user
    student = get_object_or_404(Student, user=user)
    course = get_object_or_404(Subject, pk=course_id)
    course.students.remove(student)
    course.quota += 1
    course.save()
    messages.success(request,"เอาโค้วต้าออกเรียบร้อย")
    return redirect("quotalist")

def logout_view(request):
    logout(request)
    messages.success(request, ("I'm out"))
    return redirect('/')
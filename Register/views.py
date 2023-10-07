from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Student
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse


# Create your views here.

def registrar(request):
    user = request.user
    student = Student.objects.get(user=user)
    return render(request, 'Register/archive.html',{
        'student': student,
        # 'add': Subject.objects.filter(student=student).all(),
        # 'not_add': Subject.objects.exclude(student=student).all(),
        # 'allcourse' : Subject.objects.all(),
    })


# def subject(request, course_id):
#     user = request.user
#     student = Student.objects.get(user=user)
#     course = get_object_or_404(Subject, id=course_id)

#     if request.method == 'POST':
#         student_name = request.POST.get('student_name')
#         student, created = Student.objects.get_or_create(name=student_name)

#         if not course.is_full() and student not in course.students.all():
#             course.students.add(student)

#     return render(request, 'enrollment/enroll.html', {'course': course})

def quota(request):
    user = request.user
    student = get_object_or_404(Student, user=user) 
    all_course = Subject.objects.all()
    return render(request, 'Register/quota.html',{
        "all_course": Subject.objects.exclude(students = student),
        'message': "กดลงวิชาไม่ได้เนื่องจากเต็ม",
        })

# def addstudent(request, course_id):
#     course = Subject.objects.get(pk=course_id)
#     user = request.user
#     print(22222222222222222222222222222222222222222222222222222222222222222222222)
#     print(course.quota)
#     if Students.objects.filter(user = user, subject = course).exists() and course.quota > 0:
#         print(555555)
#         student, created = Students.objects.get_or_create(user=user)
#         print(Students.objects.get_or_create(user=user))
#         student.subject.add(student)
#         course.quota -= 1
#         course.save()
#         print(111111111111111111111111111111111111111111111111111111111111111111)

#     return redirect('quota')
def add_student(request, course_id):
    user = request.user
    student = get_object_or_404(Student, user=user) 
    course = get_object_or_404(Subject, pk=course_id)

    if request.method == "POST":
        if 0 >= course.quota:
            return render(request, "Register/quota.html", {
                'message': 'โค้วต้าเต็ม',
                'all_course': Subject.objects.all()
            })
        else:
            course.students.add(student)
            course.quota -= 1
            course.save()
            return render(request, "Register/quota.html", {
                'message': 'Success',
                'all_course': Subject.objects.exclude(students = student)
            })

    # Handle the GET request here if needed
    return HttpResponseRedirect(reverse('quota'))

# def add_student(request, course_id):
    # user = request.user
    # student = get_object_or_404(Student, user=user)
    # if request.method == "POST":
    #     print(2)
    #     course = Subject.objects.get(pk=course_id)
    #     print(course)  # Change to appropriate field name
    #     course = get_object_or_404(Subject, =course)
    #     print(course)
    #     print(3)
    #     if course.max_quota <= course.quota:
    #         print(3)
    #         return render(request, "Register/quota.html", {
    #             'message' : 'โค้วต้าเต็ม'
    #         })
    #     else:
    #         print(3)
    #         course.students.add(student)
    #         course.quota += 1
    #         course.save()
    #         return render (request, "Register/quota.html",{
    #             'message' : 'Success',
    #         })
    # else:
    #     print(3)
    #     return render (request, "Register/quota.html")

# def remove_student_from_course(request, student_id, course_id):
#     student = get_object_or_404(Student, id=student_id)
#     course = get_object_or_404(Subject, id=course_id)

#     try:
#         # Remove the student from the course
#         course.students.remove(student)
#         message = f"{student.name} {student.surname} has been removed from {course.course}."
#         return JsonResponse({'message': message})

#     except Student.DoesNotExist:
#         message = "The student or course does not exist."
#         return JsonResponse({'message': message}, status=400)

# def quotalist(request):
#     all_course = Subject.objects.all()
#     user = request.user
#     # subject = Subject.objects.filter(student = user)
#     quota_list= Subject.objects.filter(students = user)
#     registered_courses = quota_list[6].all_course.all() if len(quota_list) != 0 else []
#     return render(request, 'Register/listquota.html',{
#         "quota_list" : quota_list,
#         "registered_courses" : registered_courses,
#         'user': user
#         })

def quotalist(request):

    all_courses = Subject.objects.all()
    user = request.user
    student = Student.objects.get(user = user)
    # for i in all_courses:
    #     print(type(i)
    enrolled_courses = Subject.objects.filter(students = student)
    # not_enrolled_courses = all_courses.exclude(students = user)

    return render(request, 'Register/listquota.html', {
        "enrolled_courses": enrolled_courses,
        # "not_enrolled_courses": not_enrolled_courses,
        'user': user
    })

def delete(request, course_id):
    user = request.user
    student = get_object_or_404(Student, user=user)
    course = get_object_or_404(Subject, pk=course_id)
    course.students.remove(student)
    course.quota += 1
    course.save()
    messages.success(request,"เอาโค้วต้าออกเรียบร้อย")
    return redirect("/listquota")

def logout_view(request):
    logout(request)
    return render(request, 'User/login.html', {
        'message': 'Logged out'
    })
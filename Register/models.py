from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    Name = models.CharField(max_length=64)
    Surname = models.CharField(max_length=64)
    Student_number = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.Student_number} {self.Name} {self.Surname} {self.user}"

class Subject(models.Model):
    course = models.CharField(max_length=128)
    id_course = models.CharField(max_length=128)
    Semester = models.CharField(max_length=64)
    Year = models.IntegerField()
    quota = models.IntegerField(default=50)
    max_quota = models.PositiveIntegerField(default=50)
    is_open = models.BooleanField(default=True)
    students = models.ManyToManyField(Student, blank=True, related_name="Subject")

    def __str__(self):
        return f"{self.course} {self.id_course} {self.Semester} {self.Year} {self.quota} {self.max_quota} {self.is_open} {self.students}"
        
    def current_enrollment(self):
        return self.students.count()

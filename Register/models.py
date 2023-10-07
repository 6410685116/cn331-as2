from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
# Create your models here.


class Student(models.Model):
    Name = models.CharField(max_length=64)
    Surname = models.CharField(max_length=64)
    Student_number = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.Student_number} {self.Name} {self.Surname}"

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
        return f"{self.course} {self.Semester} {self.Year}"
        
    def current_enrollment(self):
        return self.students.count()

    
# class Quota(models.Model):
#     ID = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="Student_number")

# class Flight(models.Model):
#     origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
#     destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
#     duration = models.IntegerField()

#     def __str__(self):
#         return f"{self.id}: {self.origin} to {self.destination}"


# class Passenger(models.Model):
#     first = models.CharField(max_length=64)
#     last = models.CharField(max_length=64)
#     flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

#     def __str__(self):
#         return f"{self.first} {self.last}"
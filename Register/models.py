from django.db import models

# Create your models here.


class Student(models.Model):
    Name = models.CharField(max_length=64)
    Surname = models.CharField(max_length=64)
    Student_number = models.IntegerField(max_length=10)


    def __str__(self):
        return f"Student numder:{self.Student_number} Name:{self.Name} {self.Surname}"

class Subject(models.Model):
    code = models.CharField(max_length=5)
    Subject = models.CharField(max_length=128)
    Semester = models.CharField(max_length=64)
    Year = models.IntegerField()

    def __str__(self):
        return f"Code:{self.code} Subject:{self.Subject} Semester:{self.Semester} Year:{self.Year}"
    
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
from django.db import models
from django.contrib.auth.models import User

LEVELS = (
        (1, 'A1'),
        (2, 'A1+'),
        (3, 'A2'),
        (4, 'A2+'),
        (5, 'B1'),
        (6, 'B1+'),
        (7, 'B2'),
        (8, 'B2+'),
        (9, 'C1'),
    )

MONTH = (
    ('Sep', "September"),
    ('Oct', "October"),
    ('Nov', "November"),
    ('Dec', "December"),
    ('Jan', "January"),
    ('Feb', "February"),
    ('Mar', "March"),
    ('Apr', "April"),
    ('May', "May"),
    ('Jun', "June"),
)

DURATION = (
    (1, "30 minutes"),
    (2, "45 minutes"),
    (3, "60 minutes"),
    (4, "90 minutes"),
)
WEEK_DAYS = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)


class Student(models.Model):
    owner = models.ForeignKey(User, related_name='students', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.EmailField()
    age = models.IntegerField()
    level = models.IntegerField(choices=LEVELS)
    student_info = models.CharField(max_length=250)
    zoom_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    owner = models.ForeignKey(User, related_name='lessons', on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=5, choices=MONTH)
    lesson_date = models.DateTimeField(auto_now_add=True)
    lesson_modified = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=250)
    google_docs_link = models.URLField(blank=True, null=True)
    duration = models.IntegerField(choices=DURATION)
    time_of_lesson = models.CharField(max_length=150)
    day_of_lesson = models.IntegerField(choices=WEEK_DAYS)
    price = models.IntegerField()

    class Meta:
        ordering = ["-lesson_date"]

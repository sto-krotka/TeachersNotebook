from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Lesson, Student


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


class LessonForm(ModelForm):
    """Form for creating a new lesson"""

    class Meta:
        model = Lesson
        fields = [
            'subject',
            'student',
            'month',
            'notes',
            'google_docs_link',
            'duration',
            'time_of_lesson',
            'day_of_lesson',
            'price',
        ]


class AddStudentForm(ModelForm):
    """form for adding a new student"""

    class Meta:
        model = Student
        fields = [
            'name',
            'phone',
            'email',
            'age',
            'level',
            'student_info',
            'zoom_url',
        ]

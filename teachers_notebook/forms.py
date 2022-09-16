from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Lesson, Student



# class LoginForm(forms.Form):
#     """a user log-in form"""
#     login = forms.CharField(max_length=30)
#     password = forms.CharField(widget=PasswordInput)


# class UserRegistrationForm(forms.ModelForm):
#     """Registration form for new users"""
#     password = forms.CharField(label='Password',
#                                widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password',
#                                 widget=forms.PasswordInput)
#
#     class Meta:
#         """Refers to build-in User model"""
#         model = User
#         fields = ['username', 'first_name', 'email']
#
#     def clean_password2(self):
#         """Ensures the user provides the same password twice"""
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']

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
            'price'
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

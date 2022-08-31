from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView
from django.shortcuts import render, reverse, redirect
from .models import Student, Lesson
from .forms import LessonForm, AddStudentForm, UserRegistrationForm
from django.db.models import Sum
from .filters import LessonIndexFilter, StudentIndexFilter


# imports regarding pagination:
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def register(request):
    """Allows registering a new user account using separate registration form.
    A new user is not saved until password is set"""

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})


def index(request):
    """Renders landing page, which provides basic information about the app and
    links to log-in and registration forms"""
    return render(request, 'teachers_notebook/index.html')


class ProfileView(View, PermissionRequiredMixin):
    """Renders a page with profile settings.
    Accessible only by logged-in users"""

    def get(self, request):
        return render(request, "teachers_notebook/profile.html")


@login_required
def home(request):
    """Renders home page with the total number of conducted
    lessons and the money earned.Displays list of students
    and a list of ten lessons ordered by date created"""
    lessons = Lesson.objects.all()
    last_ten = Lesson.objects.filter().order_by('-id')[:10]
    students = Student.objects.all()
    total_students = students.count()
    total_lessons = lessons.count()
    total_money = Lesson.objects.filter(
        price__isnull=False) \
        .aggregate(Sum('price'))
    context = {'students': students,
               'lessons': last_ten,
               'total_lessons': total_lessons,
               "total_students": total_students,
               "money_display": total_money}
    return render(request, 'teachers_notebook/dashboard.html', context)


@login_required
def student_details(request, pk):
    """Shows information about a student.
    Requires primary key (pk) of the given student.
    Provides lessons filtering."""
    student = Student.objects.get(id=pk)
    lessons = student.lesson_set.all()
    lessons_count = lessons.count()
    student_filter = StudentIndexFilter(request.GET, queryset=lessons)
    lessons = student_filter.qs

    # pagination disabled due to filtering issues
    # page = request.GET.get('page', 1)
    # paginator = Paginator(lessons, 10)
    # try:
    #     lessons = paginator.page(page)
    # except PageNotAnInteger:
    #     lessons = paginator.page(1)
    # except EmptyPage:
    #     lessons = paginator.page(paginator.num_pages)

    context = {'student': student,
               'lessons': lessons,
               'lessons_count': lessons_count,
               'student_filter': student_filter}

    # pagination context:
    #  'page': page,
    #  'paginator': paginator

    return render(request,
                  'teachers_notebook/student_details.html',
                  context)


@csrf_exempt
def add_lesson(request, pk):
    """Allows to add a new lesson to the database
    of a particular student. Input requires primary key
    of the student"""
    student = Student.objects.get(id=pk)
    form = LessonForm(initial={'student': student})
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/student/{student.pk}')

    context = {'form': form}
    return render(request, 'teachers_notebook/lesson_form.html', context)


class UpdateLesson(UpdateView, PermissionRequiredMixin):
    """Django generic view for modifying created lesson"""
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

    def get_context_data(self, **kwargs):
        """Retrieves data about the student from the database"""
        context = super(UpdateLesson, self).get_context_data()
        return context

    def get_success_url(self):
        """After submitting modifications sends to home page"""
        return reverse("home")


class DeleteLesson(DeleteView, PermissionRequiredMixin):
    """Django generic view for removing a created lesson"""
    model = Lesson

    def get_context_data(self, **kwargs):
        """Retrieves data about the student from the database"""
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy("home")

    """After deleting student redirects to home page"""


@csrf_exempt
def add_student(request):
    """Renders a form for creating and saving a new student
    Redirects to the detailed view of the newly added student"""
    form = AddStudentForm
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            student = Student.objects.last()
            return redirect(f'/student/{student.pk}/')
    context = {'form': form}
    return render(request, 'teachers_notebook/student_form.html', context)


class UpdateStudent(UpdateView, PermissionRequiredMixin):
    """Django generic view for modifying information about the student"""
    model = Student
    fields = [
        "name",
        "phone",
        "email",
        "age",
        "level",
        "student_info",
        "zoom_url",
    ]

    def get_context_data(self, **kwargs):
        """Retrieves the student info form the database"""
        context = super(UpdateStudent, self).get_context_data()
        return context

    def get_success_url(self):
        """Navigates the user to the student page."""
        return reverse('student', args=[self.object.pk])


class DeleteStudent(DeleteView, PermissionRequiredMixin):
    """Django generic view for removing a particular student"""
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    """Retrieves information about the student"""

    def get_success_url(self):
        return reverse_lazy("home")

    """Navigates the user to home page after deleting the student"""


@csrf_exempt
def lesson_index(request):
    """Provides a list of all conducted lessons with a filter
    to display lessons by month"""
    lessons = Lesson.objects.all()
    index_filter = LessonIndexFilter(request.GET, queryset=lessons)
    lessons = index_filter.qs
    # pagination disabled due to filtering issues
    # page = request.GET.get('page', 1)
    # paginator = Paginator(lessons, 10)
    # try:
    #     lessons = paginator.page(page)
    # except PageNotAnInteger:
    #     lessons = paginator.page(1)
    # except EmptyPage:
    #     lessons = paginator.page(paginator.num_pages)
    return render(request,
                  'teachers_notebook/lesson_index.html',
                  {'lessons': lessons, 'index_filter': index_filter})

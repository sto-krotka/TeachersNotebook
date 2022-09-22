from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.shortcuts import render, reverse, redirect
from .models import Student, Lesson
from .forms import LessonForm, AddStudentForm, SignUpForm
from django.db.models import Sum
from .filters import LessonIndexFilter, StudentIndexFilter
from django.shortcuts import get_object_or_404


class SignUpView(View):
    """Allows registering a new user account using separate registration form.
    A new user is not saved until password is set"""
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {'form': form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user,
                                password=raw_password)
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class LandingPageView(TemplateView):
    """Renders landing page, which provides basic information about the app and
      links to log-in and registration forms"""
    template_name = 'teachers_notebook/index.html'


class ProfileView(LoginRequiredMixin, View):
    """Renders a page with profile settings.
    Accessible only by logged-in users"""

    def get(self, request, *args, **kwargs):
        return render(request, "teachers_notebook/profile.html")


class HomeView(LoginRequiredMixin, View):
    """Renders home page with the total number of conducted
    lessons and the money earned.Displays list of students
    and a list of ten lessons ordered by date created"""

    def get(self, request, *args, **kwargs):
        lessons = Lesson.objects.filter(owner_id=request.user).all()
        last_ten = Lesson.objects.filter(owner_id=request.user).order_by('-id')[:10]
        students = Student.objects.filter(owner_id=request.user).all()
        total_students = students.filter(owner_id=request.user).count()
        total_lessons = lessons.filter(owner_id=request.user).count()
        total_money = Lesson.objects.filter(price__isnull=False, owner_id=request.user).aggregate(Sum('price'))
        context = {'students': students,
                   'lessons': last_ten,
                   'total_lessons': total_lessons,
                   'total_students': total_students,
                   'money_display': total_money}
        return render(request, 'teachers_notebook/dashboard.html', context)


class StudentDetailsView(LoginRequiredMixin, View):
    """Shows information about a student.
    Requires primary key (pk) of the given student.
    Provides lessons filtering."""

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        student = Student.objects.get(id=pk)
        lessons = student.lesson_set.all()
        lessons_count = lessons.count()
        student_filter = StudentIndexFilter(request.GET, queryset=lessons)
        lessons = student_filter.qs
        page = request.GET.get('page', 1)
        paginator = Paginator(lessons, 10)
        try:
            lessons = paginator.page(page)
        except PageNotAnInteger:
            lessons = paginator.page(1)
        except EmptyPage:
            lessons = paginator.page(paginator.num_pages)

        context = {'student': student,
                   'lessons': lessons,
                   'lessons_count': lessons_count,
                   'student_filter': student_filter,
                   'page': page,
                   'paginator': paginator}
        return render(request, 'teachers_notebook/student_details.html', context)


class AddLessonView(LoginRequiredMixin, View):
    """Allows to add a new lesson to the database
    of a particular student. Input requires primary key
    of the student"""
    form_class = LessonForm
    template_name = 'teachers_notebook/lesson_form.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        student = get_object_or_404(Student, pk=pk)
        student = Student.objects.filter(owner=request.user).get(id=pk)
        form = self.form_class(initial={'student': student})
        context = {'form': form,
                   'student': student}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        student = get_object_or_404(Student, pk=pk)
        student = Student.objects.filter(owner=request.user).get(id=pk)
        lessons = student.lesson_set.all()
        lessons_count = lessons.count()
        student_filter = StudentIndexFilter(request.GET, queryset=lessons)
        lessons = student_filter.qs
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)
            instance.owner = request.user
            instance.save()
        context = {'student': student,
                   'lessons': lessons,
                   'lessons_count': lessons_count + 1,
                   'student_filter': student_filter,
                   'id': pk}
        return render(request, 'teachers_notebook/student_details.html', context)


class UpdateLesson(LoginRequiredMixin, UpdateView):
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


class DeleteLesson(LoginRequiredMixin, DeleteView):
    """Django generic view for removing a created lesson"""
    model = Lesson

    def get_context_data(self, **kwargs):
        """Retrieves data about the student from the database"""
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy("home")

    """After deleting student redirects to home page"""


class AddStudentView(LoginRequiredMixin, View):
    """Renders a form for creating and saving a new student
    Redirects to the detailed view of the newly added student"""
    form_class = AddStudentForm
    template_name = 'teachers_notebook/student_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)
            instance.owner = request.user
            instance.save()
        student = Student.objects.filter(owner_id=request.user).last()
        lessons = student.lesson_set.all()
        lessons_count = lessons.count()
        student_filter = StudentIndexFilter(request.GET, queryset=lessons)
        lessons = student_filter.qs
        context = {'student': student,
                   'lessons': lessons,
                   'lessons_count': lessons_count,
                   'student_filter': student_filter,
                   'id': student.pk}
        return render(request, 'teachers_notebook/student_details.html', context)


class UpdateStudent(LoginRequiredMixin, UpdateView):
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


class DeleteStudent(LoginRequiredMixin, DeleteView):
    """Django generic view for removing a particular student"""
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    """Retrieves information about the student"""

    def get_success_url(self):
        return reverse_lazy("home")


class LessonIndexView(LoginRequiredMixin, View):
    """Provides a list of all conducted lessons with a filter
    to display lessons by month"""

    def get(self, request, *args, **kwargs):
        lessons = Lesson.objects.filter(owner_id=request.user).all()
        index_filter = LessonIndexFilter(request.GET, queryset=lessons)
        lessons = index_filter.qs
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        page = request.GET.get('page', 1)
        paginator = Paginator(lessons, 10)
        try:
            lessons = paginator.page(page)
        except PageNotAnInteger:
            lessons = paginator.page(1)
        except EmptyPage:
            lessons = paginator.page(paginator.num_pages)
        return render(request,
                      'teachers_notebook/lesson_index.html',
                      {'lessons': lessons, 'index_filter': index_filter, 'parameters': parameters})

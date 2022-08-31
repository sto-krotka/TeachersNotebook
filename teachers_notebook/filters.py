import django_filters
from .models import Lesson


class LessonIndexFilter(django_filters.FilterSet):
    """Django generic filter for displaying lessons conduced
    in a given month"""
    class Meta:
        model = Lesson
        fields = ['student', 'month']


class StudentIndexFilter(django_filters.FilterSet):
    """Django generic case-insensitive filter for searching lessons
    by month, lesson subject or notes"""
    class Meta:
        model = Lesson
        fields = {
            'subject': ['icontains'],
            'notes': ['icontains'],
            'month': ['exact'],
        }

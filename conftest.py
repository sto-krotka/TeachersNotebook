import pytest
from teachers_notebook.models import Student, Lesson


@pytest.fixture
def student():
    student1 = Student.objects.create(
        name='Anna Nowak',
        phone='678 - 675 - 432',
        email='anna@nowak.pl',
        age=19,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )
    return student1


@pytest.fixture
def lesson():
    lesson1 = Lesson.objects.create(
        subject="1.2.Grammar",
        student=Student.objects.get(pk=1),
        month='Sep',
        notes='check homework',
        google_docs_link='https://en.wikipedia.org/wiki/URL',
        duration=2,
        time_of_lesson='17:00',
        day_of_lesson=4,
        price=60,
    )
    return lesson1


@pytest.fixture
def students():
    student1 = Student.objects.create(
        name='Anna Nowak',
        phone='678 - 675 - 432',
        email='anna@nowak.pl',
        age=19,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )
    student2 = Student.objects.create(
        name='Jan Nowak',
        phone='678 - 675 - 432',
        email='jan@nowak.pl',
        age=20,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )
    student3 = Student.objects.create(
        name='Marta Kowalska',
        phone='678 - 675 - 432',
        email='jan@nowak.pl',
        age=21,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )
    return student1, student2, student3


@pytest.fixture
def lessons():
    student1 = Student.objects.create(
        name='Marta Kowalska',
        phone='678 - 675 - 432',
        email='jan@nowak.pl',
        age=21,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )
    lesson1 = Lesson.objects.create(
        subject='7.5. Grammar',
        student=Student.objects.get(pk=student1.pk),
        month='Sep',
        notes='check homework p. 100',
        google_docs_link='https://en.wikipedia.org/wiki/URL',
        duration=4,
        time_of_lesson='17:30',
        day_of_lesson=3,
        price=75,
    )
    student2 = Student.objects.create(
        name='Jan Nowak',
        phone='678 - 675 - 432',
        email='jan@nowak.pl',
        age=20,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL', )

    lesson2 = Lesson.objects.create(
        subject='7.1. Vocabulary',
        student=Student.objects.get(pk=student2.pk),
        month='Sep',
        notes='check homework p. 100',
        google_docs_link='https://en.wikipedia.org/wiki/URL',
        duration=4,
        time_of_lesson='17:30',
        day_of_lesson=3,
        price=75,
    )
    student3 = Student.objects.create(
        name='Marta Kowalska',
        phone='678 - 675 - 432',
        email='jan@nowak.pl',
        age=21,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )
    lesson3 = Lesson.objects.create(
        subject='6.6. Speaking',
        student=Student.objects.get(pk=student3.pk),
        month='Sep',
        notes='check homework p. 100',
        google_docs_link='https://en.wikipedia.org/wiki/URL',
        duration=4,
        time_of_lesson='17:30',
        day_of_lesson=3,
        price=75,
    )

    return lesson1, lesson2, lesson3

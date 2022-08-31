import pytest
from django.contrib.auth.models import User
from .models import Student, Lesson


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('Jan', 'jan@mail.com', 'johnpassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_profile_view(client):
    client.login(username='anna==', password='1234')
    response = client.get('/profile/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
    response = client.post('/logout/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_details_view(client, student):
    client.login(username='anna', password='1234')
    response = client.get(f"/student/{student.pk}/")
    assert student.name == 'Anna Nowak'
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_lesson(client, student, lesson):
    data = {
        'subject': '1.2.Grammar',
        'student': student.pk,
        'month': 'Sep',
        'notes': 'check homework',
        'google_docs_links': 'https://en.wikipedia.org/wiki/URL',
        'duration': 2,
        'time_of_lesson': '17:00',
        'day_of_lesson': 4,
        'price': 60
    }
    response = client.post(f"/add-lesson/{student.pk}/", data)
    assert response.status_code == 302
    assert Lesson.objects.get(
        subject="1.2.Grammar",
        student=student.pk,
        month='Sep',
        notes='check homework',
        google_docs_link='https://en.wikipedia.org/wiki/URL',
        duration=2,
        time_of_lesson='17:00',
        day_of_lesson=4,
        price=60,
    )


@pytest.mark.django_db
def test_add_student(client, student):
    data = {
        'name': 'Anna Nowak',
        'phone': '678 - 675 - 432',
        'email': 'anna@nowak.pl',
        'age': 19,
        'level': 7,
        'student_info': 'very ambitious',
        'zoom_url': 'https://en.wikipedia.org/wiki/URL'
    }
    response = client.post('/add-student/', data)
    assert response.status_code == 302
    assert Student.objects.get(
        name='Anna Nowak',
        phone='678 - 675 - 432',
        email='anna@nowak.pl',
        age=19,
        level=7,
        student_info='very ambitions',
        zoom_url='https://en.wikipedia.org/wiki/URL',
    )


@pytest.mark.django_db
def test_lesson_index(client, lessons):
    response = client.get('/lesson-index/')
    lessons = Lesson.objects.all()
    assert response.status_code == 302
    assert lessons.count() == 3


@pytest.mark.django_db
def test_home(client, lessons):
    response = client.get("/home/")
    students = Student.objects.all()
    lessons = Lesson.objects.all()
    assert students.all()
    assert lessons.count() == 3
    assert response.status_code == 302

import random
from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from ...models import Student, Lesson
from django.contrib.auth.models import User


MONTHS = [
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
]


class Provider(faker.providers.BaseProvider):
    def months(self):
        return self.random_element(MONTHS)


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        fake = Faker(["en_US"])
        fake.add_provider(Provider)

        # for _ in range(15):
        #     owner = User.objects.get(username='User1')
        #     name = fake.name()
        #     phone = fake.phone_number()
        #     email = fake.email()
        #     age = random.randint(10, 70)
        #     level = random.randint(1, 9)
        #     student_info = fake.text(max_nb_chars=100)
        #     zoom_url = fake.url()
        #     Student.objects.create(
        #         owner=owner,
        #         name=name,
        #         phone=phone,
        #         email=email,
        #         age=age,
        #         level=level,
        #         student_info=student_info,
        #         zoom_url=zoom_url,
        #     )
        for _ in range(15):
            owner = User.objects.get(username='User1')
            student_id = random.randint(1, 15)
            subject = fake.text(max_nb_chars=50)
            month = fake.months()
            notes = fake.text(max_nb_chars=50)
            google_docs_link = fake.url()
            duration = random.randint(1, 4)
            time_of_lesson = fake.time()
            day_of_lesson = random.randint(1, 7)
            price = random.randint(30, 90)
            Lesson.objects.create(
                owner=owner,
                subject=subject,
                student_id=student_id,
                month=month,
                notes=notes,
                google_docs_link=google_docs_link,
                duration=duration,
                time_of_lesson=time_of_lesson,
                day_of_lesson=day_of_lesson,
                price=price
            )
            check_students = Student.objects.all().count()
            self.stdout.write(self.style.SUCCESS(f'Number of students: {check_students}'))

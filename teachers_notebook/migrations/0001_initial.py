# Generated by Django 4.1 on 2022-09-16 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
                ('level', models.IntegerField(choices=[(1, 'A1'), (2, 'A1+'), (3, 'A2'), (4, 'A2+'), (5, 'B1'), (6, 'B1+'), (7, 'B2'), (8, 'B2+'), (9, 'C1')])),
                ('student_info', models.CharField(max_length=250)),
                ('zoom_url', models.URLField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=250)),
                ('month', models.CharField(choices=[('Sep', 'September'), ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December'), ('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'), ('Apr', 'April'), ('May', 'May'), ('Jun', 'June')], max_length=5)),
                ('lesson_date', models.DateTimeField(auto_now_add=True)),
                ('lesson_modified', models.DateTimeField(auto_now=True)),
                ('notes', models.CharField(max_length=250)),
                ('google_docs_link', models.URLField(blank=True, null=True)),
                ('duration', models.IntegerField(choices=[(1, '30 minutes'), (2, '45 minutes'), (3, '60 minutes'), (4, '90 minutes')])),
                ('time_of_lesson', models.CharField(max_length=150)),
                ('day_of_lesson', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('price', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons_created', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers_notebook.student')),
            ],
            options={
                'ordering': ['lesson_date'],
            },
        ),
    ]

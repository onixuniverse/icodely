# Generated by Django 4.2.5 on 2023-10-13 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_statistics', '0013_userstatistics_is_homework_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatistics',
            name='last_time_lesson_opened',
            field=models.DateTimeField(auto_now=True, verbose_name='Последний заход на урок (не менять)'),
        ),
    ]

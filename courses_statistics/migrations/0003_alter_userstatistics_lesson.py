# Generated by Django 4.2.4 on 2023-09-24 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0020_alter_course_author_alter_course_backplate_color_and_more'),
        ('courses_statistics', '0002_remove_userstatistics_homework_userstatistics_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatistics',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson',
                                    verbose_name='Урок'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-20 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('examination', '0005_remove_examination_lesson'),
        ('courses', '0015_deadlines'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='exam_homework',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='homework_url',
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63, verbose_name='Имя Д/З')),
                ('description', models.TextField(max_length=255, verbose_name='Описание')),
                ('homework_file',
                 models.FileField(blank=True, default=None, null=True, upload_to='uploads/homework/files/',
                                  verbose_name='Файл с Д/З')),
                ('homework_url', models.CharField(blank=True, max_length=127, null=True, verbose_name='Ссылка на Д/З')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                           to='examination.examination')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='homework',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='courses.homework', verbose_name='Д/З'),
        ),
    ]

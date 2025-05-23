# Generated by Django 4.2.4 on 2023-08-31 11:20

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackplateCourseColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15, verbose_name='Название цвета')),
                ('code_name', models.CharField(max_length=15, verbose_name='Код цвета')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63, verbose_name='Название курса')),
                ('description', models.TextField(blank=True, max_length=1023, verbose_name='Описание курса')),
                ('is_available', models.BooleanField(default=True, verbose_name='Курс доступен сразу?')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена за весь курс')),
                ('is_free', models.BooleanField(default=False, verbose_name='Бесплатный курс?')),
                ('backplate_color', models.CharField(
                    choices=[('yellow', 'Желтый'), ('pink', 'Розовый'), ('blue', 'Голубой'), ('gray', 'Серый')],
                    default='gray', max_length=6, verbose_name='Цвет фона')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='InviteUrl',
            fields=[
                ('invite_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,
                                                 verbose_name='UUID ссылки')),
            ],
            options={
                'verbose_name': 'Приглашение',
                'verbose_name_plural': 'Приглашения',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1023, verbose_name='Описание шага урока')),
                ('title', models.CharField(max_length=63, verbose_name='Название шага урока')),
                ('content', models.TextField(max_length=4095, verbose_name='Контент шага урока')),
                ('video_youtube', models.CharField(blank=True, default=None, max_length=127, null=True,
                                                   verbose_name='Ссылка на видео с Youtube')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
        migrations.CreateModel(
            name='UserToCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course',
                                             verbose_name='Курс')),
                ('invite_uuid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courses.inviteurl',
                                                  verbose_name='UUID приглашения(ссылки)')),
            ],
            options={
                'verbose_name': 'Доступ пользователя к курсу',
                'verbose_name_plural': 'Доступы пользователей к курсам',
            },
        ),
    ]

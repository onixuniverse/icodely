# Generated by Django 4.2.4 on 2023-09-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0012_remove_lesson_description_lesson_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=57, verbose_name='Название шага урока'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video_youtube',
            field=models.CharField(blank=True, default=None, max_length=127, null=True,
                                   verbose_name='EMBED-ссылка на видео с Youtube'),
        ),
    ]

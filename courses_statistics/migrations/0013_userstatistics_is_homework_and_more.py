# Generated by Django 4.2.5 on 2023-10-13 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_statistics', '0012_userstatistics_is_lesson_opened_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatistics',
            name='is_homework',
            field=models.BooleanField(default=False, verbose_name='Имеет Д/З? (не менять)'),
        ),
        migrations.AddField(
            model_name='userstatistics',
            name='is_homework_has_exam',
            field=models.BooleanField(default=False, verbose_name='Имеет тест в Д/З? (не менять)'),
        ),
        migrations.AddField(
            model_name='userstatistics',
            name='is_written_homework',
            field=models.BooleanField(default=False, verbose_name='Имеет письменную Д/З? (не менять)'),
        ),
        migrations.AlterField(
            model_name='userstatistics',
            name='status',
            field=models.CharField(default='Доступен', max_length=15, verbose_name='Статус'),
        ),
    ]

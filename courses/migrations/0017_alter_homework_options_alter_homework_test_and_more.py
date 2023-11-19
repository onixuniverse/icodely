# Generated by Django 4.2.4 on 2023-09-20 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('examination', '0005_remove_examination_lesson'),
        ('courses', '0016_remove_lesson_exam_homework_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homework',
            options={'verbose_name': 'Домашняя работа', 'verbose_name_plural': 'Домашние работы'},
        ),
        migrations.AlterField(
            model_name='homework',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='examination.examination', verbose_name='Тестирование'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='title',
            field=models.CharField(max_length=63, verbose_name='Название Д/З'),
        ),
    ]

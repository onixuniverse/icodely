# Generated by Django 4.2.4 on 2023-09-24 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses_statistics', '0003_alter_userstatistics_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatistics',
            name='attempts',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Количество попыток'),
        ),
    ]

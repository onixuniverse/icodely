# Generated by Django 4.2.4 on 2023-09-24 13:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses_statistics', '0004_userstatistics_attempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatistics',
            name='attempts',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Количество попыток'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0009_alter_usertocourse_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='pdf_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='uploads/lessons/pdf/',
                                   verbose_name='PDF-файл'),
        ),
    ]

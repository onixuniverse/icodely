# Generated by Django 4.2.5 on 2023-10-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('examination', '0010_examinationanswer_is_answer_right'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationquestion',
            name='question',
            field=models.TextField(max_length=1023, verbose_name='Вопрос'),
        ),
    ]

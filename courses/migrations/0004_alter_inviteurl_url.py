# Generated by Django 4.2.4 on 2023-09-02 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0003_inviteurl_url_alter_inviteurl_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inviteurl',
            name='url',
            field=models.CharField(default='https://icodely.ru/invite?url=009064e8-07c9-4f64-a80e-c048010996e1',
                                   max_length=127),
        ),
    ]

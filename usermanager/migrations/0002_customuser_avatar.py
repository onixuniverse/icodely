# Generated by Django 4.2.4 on 2023-08-31 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='media/default_media/avatars/', upload_to='media/usermanager/avatars/'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-31 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='default/avatars/user_avatar.png', upload_to='users/avatars/'),
        ),
    ]

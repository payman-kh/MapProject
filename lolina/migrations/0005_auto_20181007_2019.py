# Generated by Django 2.1.1 on 2018-10-07 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lolina', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

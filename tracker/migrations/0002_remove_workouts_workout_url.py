# Generated by Django 2.1 on 2019-01-03 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workouts',
            name='workout_url',
        ),
    ]

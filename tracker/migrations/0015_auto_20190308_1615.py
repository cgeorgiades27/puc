# Generated by Django 2.1.5 on 2019-03-08 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_auto_20190207_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workouts',
            name='workout_title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

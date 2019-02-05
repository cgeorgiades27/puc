# Generated by Django 2.1.3 on 2019-02-01 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_exercise_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='routine',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routine', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.1.3 on 2019-01-31 13:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalReps', models.IntegerField(validators=[django.core.validators.MaxValueValidator(999999)])),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compName', models.CharField(max_length=50)),
                ('startDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('endDate', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999)])),
                ('sets', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                ('weight', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999)])),
                ('date_entered', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_completed', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_url', models.TextField(blank=True, default='https://bankwatch.org/wp-content/uploads/2018/03/Portrait_Placeholder.png', max_length=150, null=True)),
                ('banner_url', models.TextField(blank=True, default='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/items/566020/bba5cf5acb1e03045d81555821b986c7461ca64c.jpg', max_length=150, null=True)),
                ('motto', models.TextField(blank=True, max_length=100, null=True)),
                ('bday', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workouts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_title', models.CharField(max_length=50)),
                ('workout_url', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='workout_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='tracker.Workouts'),
        ),
        migrations.AddField(
            model_name='compentry',
            name='compName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition', to='tracker.Competition'),
        ),
        migrations.AddField(
            model_name='compentry',
            name='workout_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Workouts'),
        ),
    ]

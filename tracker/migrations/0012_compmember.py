# Generated by Django 2.1.5 on 2019-02-06 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0011_auto_20190116_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compMember', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('compName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Competition')),
            ],
        ),
    ]
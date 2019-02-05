# Generated by Django 2.1.3 on 2019-02-04 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_auto_20190201_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='compName',
        ),
        migrations.AlterField(
            model_name='routine',
            name='exercise',
            field=models.ManyToManyField(related_name='ex', to='tracker.Exercise', verbose_name='add exercises'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='name',
            field=models.CharField(max_length=50, verbose_name='routine name'),
        ),
    ]

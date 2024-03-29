# Generated by Django 2.1.3 on 2019-01-15 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='banner_url',
            field=models.TextField(blank=True, default='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/items/566020/bba5cf5acb1e03045d81555821b986c7461ca64c.jpg', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic_url',
            field=models.TextField(blank=True, default='https://bankwatch.org/wp-content/uploads/2018/03/Portrait_Placeholder.png', max_length=100, null=True),
        ),
    ]

# Generated by Django 2.2 on 2020-03-04 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], default='1'),
        ),
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 4, 15, 41, 1, 109507)),
        ),
    ]
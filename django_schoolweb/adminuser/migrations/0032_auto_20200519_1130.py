# Generated by Django 2.2 on 2020-05-19 11:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0031_auto_20200518_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 11, 30, 0, 772499)),
        ),
    ]

# Generated by Django 2.2 on 2020-03-08 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0022_auto_20200307_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 8, 17, 9, 45, 747425)),
        ),
    ]

# Generated by Django 2.2 on 2020-05-19 22:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0034_auto_20200519_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 22, 19, 59, 642674)),
        ),
    ]

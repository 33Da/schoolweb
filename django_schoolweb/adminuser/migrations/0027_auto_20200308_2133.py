# Generated by Django 2.2 on 2020-03-08 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0026_auto_20200308_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 8, 21, 33, 27, 6735)),
        ),
    ]

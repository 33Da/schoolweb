# Generated by Django 2.2 on 2020-03-05 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0010_auto_20200305_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 5, 19, 57, 26, 612886)),
        ),
    ]
# Generated by Django 2.2 on 2020-03-06 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0013_auto_20200305_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='political',
            field=models.IntegerField(choices=[(0, '群众'), (1, '共青团员'), (2, '中共预备党员'), (3, '中共党员'), (4, '其它党派')], default='1'),
        ),
        migrations.AlterField(
            model_name='user',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 6, 18, 8, 8, 768158)),
        ),
    ]

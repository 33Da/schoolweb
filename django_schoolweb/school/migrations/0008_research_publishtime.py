# Generated by Django 2.2 on 2020-03-05 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_auto_20200305_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='publishtime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 2.2 on 2020-05-18 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0017_auto_20200518_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='abstract',
            field=models.TextField(blank=True, null=True),
        ),
    ]
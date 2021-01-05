# Generated by Django 2.2 on 2020-03-05 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20200305_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchfile',
            name='url',
            field=models.FileField(upload_to='research/file/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='researchpic',
            name='url',
            field=models.ImageField(max_length=1000, upload_to='research/pic/%Y/%m/'),
        ),
    ]

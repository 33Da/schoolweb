# Generated by Django 2.2 on 2020-03-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_auto_20200305_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsfile',
            name='url',
            field=models.FileField(upload_to='news/file/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='newspic',
            name='url',
            field=models.ImageField(max_length=1000, upload_to='news/pic/%Y/%m/'),
        ),
    ]

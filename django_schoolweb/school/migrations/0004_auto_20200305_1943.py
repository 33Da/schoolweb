# Generated by Django 2.2 on 2020-03-05 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20200305_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsfile',
            name='url',
            field=models.FileField(upload_to='media/news/file/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='newspic',
            name='url',
            field=models.ImageField(max_length=1000, upload_to='media/news/pic/%Y/%m/'),
        ),
    ]

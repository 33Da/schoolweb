# Generated by Django 2.2 on 2020-03-05 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_news_publishtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsfile',
            name='url',
            field=models.FileField(upload_to='media/new/file/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='newspic',
            name='url',
            field=models.ImageField(max_length=1000, upload_to='media/new/pic/%Y/%m/'),
        ),
    ]
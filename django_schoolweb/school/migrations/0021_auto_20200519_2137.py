# Generated by Django 2.2 on 2020-05-19 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0020_match_enclosure_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teams',
            name='no_pass',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
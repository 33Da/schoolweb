# Generated by Django 2.2 on 2020-05-18 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_match_abstract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='sum_team_num',
            new_name='nocheck_team_num',
        ),
        migrations.AddField(
            model_name='match',
            name='history_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
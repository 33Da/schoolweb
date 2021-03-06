# Generated by Django 2.2 on 2020-05-19 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0021_auto_20200519_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team_students',
            name='teacher_name',
        ),
        migrations.RemoveField(
            model_name='team_students',
            name='teacher_phone',
        ),
        migrations.AddField(
            model_name='teams',
            name='teacher_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='teams',
            name='teacher_phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='team_students',
            name='role',
            field=models.IntegerField(choices=[(0, '队长'), (1, '队员')], default=0),
        ),
    ]

# Generated by Django 2.2 on 2020-03-08 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0013_subject_credit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='read_type',
            new_name='readtype',
        ),
    ]
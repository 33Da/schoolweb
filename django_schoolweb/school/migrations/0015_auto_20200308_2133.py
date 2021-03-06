# Generated by Django 2.2 on 2020-03-08 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_auto_20200308_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='readtype',
            field=models.IntegerField(choices=[(1, '选修'), (2, '必修')], default=1),
        ),
        migrations.AlterField(
            model_name='subject',
            name='type',
            field=models.IntegerField(choices=[(1, '公共课'), (2, '实践课'), (3, '通识课')], default=0),
        ),
        migrations.AlterField(
            model_name='userandsubject',
            name='exam_grade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userandsubject',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userandsubject',
            name='usually_grade',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

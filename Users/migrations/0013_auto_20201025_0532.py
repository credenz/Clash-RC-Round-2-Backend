# Generated by Django 3.1.2 on 2020-10-25 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0012_auto_20201024_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='constraints',
            field=models.TextField(default='NA'),
        ),
        migrations.AddField(
            model_name='questions',
            name='explanation',
            field=models.TextField(default='NA'),
        ),
        migrations.AddField(
            model_name='questions',
            name='iformat',
            field=models.TextField(default='NA'),
        ),
        migrations.AddField(
            model_name='questions',
            name='oformat',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='sampleInput',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='sampleOutput',
            field=models.TextField(default='NA'),
        ),
    ]

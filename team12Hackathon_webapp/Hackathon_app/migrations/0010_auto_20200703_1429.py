# Generated by Django 3.0.8 on 2020-07-03 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hackathon_app', '0009_kindiconfeature_typeimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kindiconfeature',
            name='Base64',
            field=models.CharField(max_length=999999),
        ),
    ]

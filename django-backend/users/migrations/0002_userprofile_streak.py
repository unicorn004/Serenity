# Generated by Django 5.1.7 on 2025-03-19 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='streak',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-21 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackUpAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bu_model',
            name='user',
            field=models.CharField(max_length=200),
        ),
    ]

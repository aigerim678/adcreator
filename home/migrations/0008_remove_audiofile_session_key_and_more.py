# Generated by Django 5.1.2 on 2024-10-27 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_scenario_temp_id_uploadedvideo_temp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofile',
            name='session_key',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='session_key',
        ),
        migrations.RemoveField(
            model_name='uploadedvideo',
            name='session_key',
        ),
    ]
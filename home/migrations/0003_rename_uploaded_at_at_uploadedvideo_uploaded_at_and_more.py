# Generated by Django 5.1.2 on 2024-10-26 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_uploadedvideo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedvideo',
            old_name='uploaded_at_at',
            new_name='uploaded_at',
        ),
        migrations.RemoveField(
            model_name='uploadedvideo',
            name='user',
        ),
    ]
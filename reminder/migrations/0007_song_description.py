# Generated by Django 5.2.3 on 2025-06-23 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0006_song_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

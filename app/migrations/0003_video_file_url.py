# Generated by Django 4.1.4 on 2022-12-12 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_video_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='file_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
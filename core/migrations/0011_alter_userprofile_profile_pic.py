# Generated by Django 4.2.7 on 2023-12-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_timelineevent_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, height_field='avatar_height', null=True, upload_to='avatars/', width_field='avatar_width'),
        ),
    ]

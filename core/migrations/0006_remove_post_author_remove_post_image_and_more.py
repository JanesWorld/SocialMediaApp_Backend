# Generated by Django 4.2.7 on 2023-11-27 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
    ]
# Generated by Django 5.1.7 on 2025-03-27 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programmingCourse', '0004_groupjoinrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='is_muted',
            field=models.BooleanField(default=False),
        ),
    ]

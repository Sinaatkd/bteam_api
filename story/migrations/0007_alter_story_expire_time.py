# Generated by Django 4.0.4 on 2022-09-16 15:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0006_alter_story_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 17, 15, 7, 8, 22884, tzinfo=utc)),
        ),
    ]

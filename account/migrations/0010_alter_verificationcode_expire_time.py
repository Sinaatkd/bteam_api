# Generated by Django 4.0.2 on 2022-05-11 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 17, 24, 38, 859647), verbose_name='زمان انقضا'),
        ),
    ]

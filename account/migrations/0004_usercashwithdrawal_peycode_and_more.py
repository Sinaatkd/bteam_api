# Generated by Django 4.0.2 on 2022-04-13 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercashwithdrawal',
            name='peycode',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 13, 15, 40, 15, 418288), verbose_name='زمان انقضا'),
        ),
    ]

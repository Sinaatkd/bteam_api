# Generated by Django 4.0.2 on 2022-04-14 11:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_peycode_usercashwithdrawal_paycode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 14, 15, 50, 22, 483769), verbose_name='زمان انقضا'),
        ),
    ]

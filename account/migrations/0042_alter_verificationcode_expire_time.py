# Generated by Django 4.0.4 on 2022-09-20 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0041_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 13, 32, 34, 248020), verbose_name='زمان انقضا'),
        ),
    ]
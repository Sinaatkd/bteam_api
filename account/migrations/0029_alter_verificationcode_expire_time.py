# Generated by Django 4.0.4 on 2022-07-09 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 10, 0, 0, 28, 44446), verbose_name='زمان انقضا'),
        ),
    ]

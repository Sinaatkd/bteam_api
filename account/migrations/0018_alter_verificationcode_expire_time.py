# Generated by Django 4.0.4 on 2022-06-24 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 13, 31, 39, 480003), verbose_name='زمان انقضا'),
        ),
    ]

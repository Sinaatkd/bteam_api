# Generated by Django 4.0.4 on 2022-09-16 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0038_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 13, 52, 1, 387006), verbose_name='زمان انقضا'),
        ),
    ]

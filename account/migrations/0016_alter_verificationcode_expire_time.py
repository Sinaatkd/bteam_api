# Generated by Django 4.0.4 on 2022-06-24 07:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 12, 25, 13, 775081), verbose_name='زمان انقضا'),
        ),
    ]

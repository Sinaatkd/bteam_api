# Generated by Django 4.0.2 on 2022-05-05 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_verificationcode_expire_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_foreigner',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 5, 17, 26, 22, 2280), verbose_name='زمان انقضا'),
        ),
    ]
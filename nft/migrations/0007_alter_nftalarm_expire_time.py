# Generated by Django 4.0.4 on 2022-09-20 09:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nft', '0006_alter_nftalarm_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nftalarm',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 9, 29, 26, 40399, tzinfo=utc)),
        ),
    ]

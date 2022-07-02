# Generated by Django 4.0.4 on 2022-06-25 08:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_userkucoinapi_alter_verificationcode_expire_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_kucoin_api',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.userkucoinapi'),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 12, 40, 3, 97759), verbose_name='زمان انقضا'),
        ),
    ]
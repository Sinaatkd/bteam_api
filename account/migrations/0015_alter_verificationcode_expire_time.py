# Generated by Django 4.0.4 on 2022-06-23 11:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_user_face_user_is_full_authentication_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 23, 16, 11, 53, 375635), verbose_name='زمان انقضا'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-24 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trade', '0003_alter_basket_blocked_users_alter_basket_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='is_accept_participant',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.0.4 on 2022-07-02 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trade', '0008_basket_trader_futures_api_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='time_of_start',
        ),
    ]
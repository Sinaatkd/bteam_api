# Generated by Django 4.0.4 on 2022-07-29 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trade', '0011_order_order_type_alter_basket_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stop_loss',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='target',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

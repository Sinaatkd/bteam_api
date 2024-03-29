# Generated by Django 4.0.4 on 2022-07-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trade', '0010_order_remove_basket_orders_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='orders',
            field=models.ManyToManyField(blank=True, to='copy_trade.order'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-24 08:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('copy_trade', '0002_basket_is_freeze_basket_orders_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, related_name='blocked_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='basket',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]

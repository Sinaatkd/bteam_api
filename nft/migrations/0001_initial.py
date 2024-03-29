# Generated by Django 4.0.4 on 2022-09-16 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NFTAlarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_price', models.FloatField()),
                ('nft_name', models.CharField(max_length=500)),
                ('nft_price', models.FloatField()),
                ('collection_name', models.CharField(max_length=500)),
                ('filter_mode', models.CharField(choices=[('24h', '24h'), ('7d', '7d'), ('30d', '30d'), ('all', 'all')], max_length=3)),
                ('nft_link', models.URLField()),
            ],
        ),
    ]

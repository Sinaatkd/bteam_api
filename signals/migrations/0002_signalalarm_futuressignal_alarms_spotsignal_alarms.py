# Generated by Django 4.0.2 on 2022-05-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignalAlarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='futuressignal',
            name='alarms',
            field=models.ManyToManyField(to='signals.SignalAlarm'),
        ),
        migrations.AddField(
            model_name='spotsignal',
            name='alarms',
            field=models.ManyToManyField(to='signals.SignalAlarm'),
        ),
    ]

from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class NFTAlarm(models.Model):
    floor_price = models.FloatField()
    nft_name = models.CharField(max_length=500)
    nft_price = models.FloatField()
    collection_name = models.CharField(max_length=500)
    filter_mode = models.CharField(choices=(('24h', '24h'), ('7d', '7d'), ('30d', '30d'), ('all', 'all')), max_length=3)
    nft_link = models.URLField()
    expire_time = models.DateTimeField(default=now() + timedelta(days=1))
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.collection_name} - {self.nft_name}'

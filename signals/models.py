from django.db import models
from base_model.models import BaseModel, IntegerRangeField
from account.models import User


class SignalAlarm(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SignalNews(BaseModel):
    content = models.CharField(max_length=120)
    seen_by = models.ManyToManyField(User)

    def __str__(self):
        return self.content


class Target(BaseModel):
    title = models.CharField(max_length=120)
    amount = models.FloatField()
    is_touched = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} -- {self.amount}'


class SpotSignal(BaseModel):
    coin_symbol = models.CharField(max_length=30)
    proposed_capital = IntegerRangeField(min_value=0, max_value=100)
    r_and_r = models.FloatField()
    type_of_investment = models.CharField(
        max_length=30, choices=[['بلند مدت', 'بلند مدت'], ['کوتاه مدت', 'کوتاه مدت']])
    profit_of_signal_amount = models.FloatField(null=True, blank=True)
    signal_news = models.ManyToManyField(SignalNews, null=True, blank=True)
    targets = models.ManyToManyField(Target)
    stop_loss = models.FloatField()
    entry = models.FloatField()
    is_touched_entry = models.BooleanField(default=False)
    status = models.CharField(max_length=250, null=True, blank=True)
    alarms = models.ManyToManyField(SignalAlarm, blank=True)

    def __str__(self):
        return self.coin_symbol


class FuturesSignal(BaseModel):
    coin_symbol = models.CharField(max_length=30)
    amount = IntegerRangeField(min_value=0, max_value=100)
    leverage = models.IntegerField()
    type_of_investment = models.CharField(
        max_length=30, choices=[['SHORT', 'SHORT'], ['LONG', 'LONG']])
    profit_of_signal_amount = models.FloatField(null=True, blank=True)
    signal_news = models.ManyToManyField(SignalNews, null=True, blank=True)
    targets = models.ManyToManyField(Target)
    stop_loss = models.FloatField()
    entry = models.FloatField()
    is_touched_entry = models.BooleanField(default=False)
    status = models.CharField(max_length=250, null=True, blank=True)
    alarms = models.ManyToManyField(SignalAlarm, blank=True)

    def __str__(self):
        return self.coin_symbol

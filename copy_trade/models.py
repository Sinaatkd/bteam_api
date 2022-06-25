from django.db import models
from account.models import User



class Stage(models.Model):
    title = models.CharField(max_length=100)
    amount = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f'{self.title} -- {self.amount}'


class Basket(models.Model):
    trader_name = models.CharField(max_length=300)
    trader_api_features = models.CharField(max_length=1000)
    trader_api_spot = models.CharField(max_length=1000)
    initial_balance = models.FloatField()
    win_rate = models.PositiveIntegerField()
    exchange = models.CharField(max_length=200, default='کوکوین')
    basket_risk = models.CharField(max_length=200)
    maximum_loss = models.PositiveIntegerField()
    maximum_profit = models.PositiveIntegerField()
    estimated_time = models.PositiveIntegerField()
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_users', blank=True)
    time_of_start = models.DateTimeField()
    stages = models.ManyToManyField(Stage)
    settlement_percentage = models.PositiveIntegerField()
    is_freeze = models.BooleanField(default=False)
    orders_type = models.CharField(max_length=10, choices=(('f', 'futures'), ('s', 'spot')), null=True, blank=True)
    is_accept_participant = models.BooleanField(default=True)


    def __str__(self) -> str:
        return f'{self.trader_name} - {self.win_rate}'
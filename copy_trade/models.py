from django.db import models
from account.models import User



class Stage(models.Model):
    title = models.CharField(max_length=100)
    amount = models.PositiveBigIntegerField()
    is_pay_time = models.BooleanField(default=False)
    pay_datetime = models.DateTimeField(null=True, blank=True)
    payers = models.ManyToManyField(User, blank=True)


    def __str__(self) -> str:
        return f'{self.title} -- {self.amount}'


class Basket(models.Model):
    trader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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
    is_active = models.BooleanField(default=True)
    orders_count = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self) -> str:
        return f'{self.trader} - {self.win_rate}'
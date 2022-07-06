from django.db import models
from account.models import User



class Stage(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    amount = models.PositiveBigIntegerField(verbose_name='مبلغ')
    is_pay_time = models.BooleanField(default=False, verbose_name='زمان پرداخت باشد')
    pay_datetime = models.DateTimeField(null=True, blank=True, verbose_name='زمان پرداخت')
    payers = models.ManyToManyField(User, blank=True, verbose_name='پرداخت کنندگان')


    def __str__(self) -> str:
        return f'{self.title} -- {self.amount}'


class Basket(models.Model):
    trader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='تریدر')
    trader_spot_api = models.CharField(max_length=1000, null=True, blank=True, verbose_name='spot api key تریدر')
    trader_spot_secret = models.CharField(max_length=1000, null=True, blank=True, verbose_name='spot secret key تریدر')
    trader_spot_passphrase = models.CharField(max_length=1000, null=True, blank=True, verbose_name='spot passphrase تریدر')
    trader_futures_api = models.CharField(max_length=1000, null=True, blank=True, verbose_name='futures api key تریدر')
    trader_futures_secret = models.CharField(max_length=1000, null=True, blank=True, verbose_name='futures secret key تریدر')
    trader_futures_passphrase = models.CharField(max_length=1000, null=True, blank=True, verbose_name='futures passphrase تریدر')
    initial_balance = models.FloatField(verbose_name='موجودی اولیه')
    win_rate = models.PositiveIntegerField(verbose_name='win rate')
    exchange = models.CharField(max_length=200, default='کوکوین', verbose_name='صرافی')
    basket_risk = models.CharField(max_length=200, verbose_name='ریسک سبد')
    maximum_loss = models.PositiveIntegerField(verbose_name='حداکثر ضرر')
    maximum_profit = models.PositiveIntegerField(verbose_name='حداکثر سود')
    estimated_time = models.PositiveIntegerField(verbose_name='زمان تخمینی')
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_users', blank=True)
    stages = models.ManyToManyField(Stage, blank=True, verbose_name='stages')
    settlement_percentage = models.PositiveIntegerField(verbose_name='درصد تسویه')
    is_freeze = models.BooleanField(default=False)
    orders_type = models.CharField(max_length=10, choices=(('f', 'futures'), ('s', 'spot')), null=True, blank=True, verbose_name='نوع سبد')
    is_accept_participant = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    orders_count = models.PositiveIntegerField(default=0)


    def __str__(self) -> str:
        return f'{self.trader} - {self.win_rate}'
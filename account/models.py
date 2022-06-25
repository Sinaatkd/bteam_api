import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from base_model.models import BaseModel


class Device(models.Model):
    uuid = models.CharField(unique=True, max_length=50, null=True, blank=True)
    platform = models.CharField(max_length=7,
                                choices=[('android', 'android'), ('web', 'web'), ('ios', 'ios')])
    model = models.CharField(max_length=100)
    operating_system = models.CharField(
        max_length=7,
        choices=[(
            'ios', 'ios'), ('android', 'android'), ('windows', 'windows'), ('mac', 'mac'), ('unknown', 'unknown')])
    os_version = models.CharField(max_length=120)

    def __str__(self):
        return self.model


class UserKucoinAPI(models.Model):
    futures_api_key = models.CharField(max_length=1000)
    futures_secret =  models.CharField(max_length=1000)
    futures_passphrase = models.CharField(max_length=1000)
    spot_api_key = models.CharField(max_length=1000)
    spot_secret =  models.CharField(max_length=1000)
    spot_passphrase = models.CharField(max_length=1000)

    def __str__(self):
        return self.futures_api_key


class User(AbstractUser):
    full_name = models.CharField(max_length=120)
    phone_number = models.PositiveBigIntegerField(
        unique=True, null=True, blank=True)
    national_code = models.PositiveBigIntegerField(
        unique=True, null=True, blank=True)
    from_city = models.CharField(max_length=300, null=True, blank=True)
    is_phone_number_verified = models.BooleanField(
        default=False, null=True, blank=True)
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE, null=True, blank=True)
    amount_of_capital = models.CharField(max_length=100, null=True, blank=True)
    familiarity_with_digital_currencies = models.CharField(
        max_length=100, null=True, blank=True)
    get_to_know_us = models.CharField(max_length=100, null=True, blank=True)
    is_receive_signal_notifications = models.BooleanField(default=True)
    is_receive_news_notifications = models.BooleanField(default=True)
    invated_users = models.ManyToManyField('self', blank=True)
    wallet = models.PositiveIntegerField(default=0)
    is_foreigner = models.BooleanField(default=False)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    place_of_issue = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = None
    last_name = None
    id_card = models.ImageField(upload_to='id_card', null=True, blank=True)
    face = models.ImageField(upload_to='id_card', null=True, blank=True)
    is_full_authentication = models.BooleanField(default=False)
    user_kucoin_api = models.OneToOneField(UserKucoinAPI, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    code = models.CharField(max_length=4, verbose_name='کد تایید')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    expire_time = models.DateTimeField(default=datetime.datetime.now(
    ) + datetime.timedelta(minutes=1), verbose_name='زمان انقضا')

    def __str__(self):
        return f'{self.user.full_name} - {self.code}'

    @property
    def is_expire(self):
        return self.expire_time < timezone.now()


class UserMessage(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserGift(BaseModel):
    gift_type = models.CharField(max_length=10,
                                 choices=[('red-b', 'red-b'), ('blue-b', 'blue-b'), ('black-b', 'black-b')])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    code = models.BigIntegerField(unique=True)
    for_what = models.CharField(choices=[('register', 'register'), ('buy', 'buy')], max_length=20, null=True,
                                blank=True)
    transaction = models.ForeignKey('transaction.Transaction', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.full_name} - {self.gift_type} - {self.code}'


class UserGiftLog(BaseModel):
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title} - {self.content}'


class UserCashWithdrawal(BaseModel):
    is_confirmation = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    bank_card_number = models.PositiveBigIntegerField()
    amount = models.PositiveIntegerField()
    paycode = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

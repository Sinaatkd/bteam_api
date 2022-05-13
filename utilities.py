import datetime
from math import ceil
import jdatetime
import os
import json
import threading
import random
import string
from random import randint
import ippanel
import requests

from django.db.models import Sum
from rest_framework.authtoken.models import Token
from account.models import VerificationCode, User
from signals.models import FuturesSignal, SpotSignal, Target


def send_sms(pattern, phone_number, variables):
    sms = ippanel.Client('gV15DLD3t2ZQyLFrC9OpGfCfsH6DlBeJkOXnF8qN9XE=')
    sms.send_pattern(pattern, '+983000505', f'+98{phone_number}', variables)


def send_sms_without_pattern(text, phone_numbers):
    sms = ippanel.Client('gV15DLD3t2ZQyLFrC9OpGfCfsH6DlBeJkOXnF8qN9XE=')
    sms.send('+989999150632', phone_numbers, text)


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext


def send_verification_code(phone):
    code = randint(1111, 9999)
    VerificationCode.objects.create(user=User.objects.get(phone_number=phone), code=code,
                                    expire_time=datetime.datetime.now() + datetime.timedelta(minutes=1))
    send_sms('hv65e9v4ne', phone, {'code': str(code)})


def generate_token(user):
    token = Token.objects.filter(user_id=user.id).first()
    if token is None:
        token = Token.objects.create(user_id=user.id)
    else:
        token.delete()
        token = Token.objects.create(user_id=user.id)
    return token


def send_to_users_iphones_or_web_platform(title, content):
    for user in User.objects.all():
        try:
            if user.device.operating_system == 'ios' or user.device.platform == 'web':
                send_sms('8vgnui3wcy', user.phone_number, {
                         'coin_symbol': title.split(' ')[1], 'content': content})
        except:
            pass


def send_notification(title, content, is_send_sms=True):
    TOKEN = '0516638bac652996d133bc0f9208882694a6e8e5'
    APP_ID = '5ej1mqy1nkorv2ye'

    url = f'https://api.pushe.co/v2/messaging/notifications/'

    headers = {
        'Authorization': f'Token {TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        'app_ids': APP_ID,
        'data': {
            'title': title,
            'content': content
        }
    })

    requests.post(url, data=payload, headers=headers)

    if is_send_sms:
        thread = threading.Thread(
            target=send_to_users_iphones_or_web_platform, args=(title, content, ))
        thread.start()

def diff_between_two_dates(d1, d2):
    date_format = "%m/%d/%Y, %H:%M:%S"
    a = d1.strftime(date_format)
    b = d2.strftime(date_format)
    d1 = datetime.datetime.strptime(str(b), date_format)
    d2 = datetime.datetime.strptime(str(a), date_format)
    delta = d2 - d1
    return delta


def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(length))


def generate_unique_gift_code():
    return int(randint(100000000000, 999999999999))


def get_now_jalali_date():
    return jdatetime.datetime.now().strftime("%Y/%m/%d")  # '1399/01/05'


def calculate_profit_of_signals(time_range):
    days = 1
    today = datetime.datetime.today()
    if time_range == 'daily':
        days = 1
    elif time_range == 'weekly':
        days = 7
    elif time_range == 'monthly':
        days = 30

    range_date = today - datetime.timedelta(days=days)

    spot_signals = SpotSignal.objects.filter(
        is_active=False, created_time__range=[range_date, today])

    futures_signals = FuturesSignal.objects.filter(
        is_active=False, created_time__range=[range_date, today])

    profit_value = 0

    for futures_signal in futures_signals:
        if (futures_signal.profit_of_signal_amount == 0):
            futures_signal.profit_of_signal_amount = -7
        profit_value += (futures_signal.amount / 100) * \
            futures_signal.profit_of_signal_amount

    for spot_signal in spot_signals:
        if (spot_signal.profit_of_signal_amount == 0):
            spot_signal.profit_of_signal_amount = -7
        profit_value += (spot_signal.proposed_capital / 100) * \
            spot_signal.profit_of_signal_amount

    return profit_value


def is_first_target_touched(signal, target):
    return signal.targets.all().first().id == target.id


def get_prev_touched_target(signal):
    return signal.targets.filter(is_touched=True).last()
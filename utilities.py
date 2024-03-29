import datetime
from math import ceil
import jdatetime
import os
import json
import threading
import random
import string
import time
import hmac
import hashlib
import base64
from random import randint
import ippanel
import requests

from rest_framework.authtoken.models import Token
from account.models import VerificationCode, User
from signals.models import FuturesSignal, SpotSignal
from transaction.models import Transaction


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
    for transaction in Transaction.objects.all():
        user = transaction.user
        if user.device.operating_system == 'ios' or user.device.platform == 'web':
            try:
                send_sms('8vgnui3wcy', user.phone_number, {
                    'coin_symbol': title.split(' ')[1], 'content': content})
            except:
                pass


def send_notification(title, content, is_send_sms=False):
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


def check_user_usdt_balance(user):
    user_kucoin_api = user.user_kucoin_api
    api_key = user_kucoin_api.spot_api_key
    api_secret = user_kucoin_api.spot_secret
    api_passphrase = user_kucoin_api.spot_passphrase
    url = 'https://api.kucoin.com/api/v1/accounts'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request('get', url, headers=headers)
    return list(filter(lambda x: x['currency'] == 'USDT' and x['type'] == 'trade', response.json()['data']))[0]


def get_balance(api_key, api_secret, api_passphrase):
    url = 'https://api.kucoin.com/api/v1/accounts'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request('get', url, headers=headers)
    return response.json()['data']


def get_user_currency_balance(api_key, api_secret, api_passphrase, symbol):
    currencies = get_balance(api_key, api_secret, api_passphrase)
    symbol = symbol.split('-')[0]
    selected_currency = list(filter(
        lambda x: x['type'] == 'trade' and x['currency'] == symbol, currencies))[0]
    return selected_currency['available']


def get_user_kucoin_apis(participant, basket):
    participant_api = participant.user_kucoin_api
    api_key = participant_api.spot_api_key if basket.orders_type == 's' else participant_api.futures_api_key
    api_secret = participant_api.spot_secret if basket.orders_type == 's' else participant_api.futures_secret
    api_passphrase = participant_api.spot_passphrase if basket.orders_type == 's' else participant_api.futures_passphrase

    return api_key, api_secret, api_passphrase


def get_all_currencies_prices(api_key, api_secret, api_passphrase):
    url = f'https://api.kucoin.com/api/v1/prices'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f'/api/v1/prices'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request('get', url, headers=headers)
    return response.json()


def copy_trade_calculate_loss_and_profit(user_balance, initial_balance):
    loss = 0
    profit = 0
    if (user_balance > float(initial_balance)):
        profit = ((user_balance - initial_balance) / initial_balance) * 100
    else:
        loss = ((user_balance - initial_balance) / initial_balance) * 100

    return float(str(loss)[:4]), float(str(profit)[:4])


def get_active_orders(order_type, api_key, api_secret, api_passphrase):
    now = int(time.time() * 1000)
    if order_type == 's':
        url = f'https://api.kucoin.com/api/v1/stop-order'
        str_to_sign = str(now) + 'GET' + f'/api/v1/stop-order'
    elif order_type == 'f':
        url = f'https://api-futures.kucoin.com/api/v1/stopOrders'
        str_to_sign = str(now) + 'GET' + f'/api/v1/stopOrders'

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        'Content-Type': 'application/json'
    }
    response = requests.request('get', url, headers=headers)
    return response.json()['data']['items']


def create_stop_order(order_type, api_key, api_secret, api_passphrase, **payload):
    payload['clientOid'] = randint(1, 10000) * 1000
    now = int(time.time() * 1000)
    data_json = json.dumps(payload)
    if order_type == 's':
        url = 'https://api.kucoin.com/api/v1/stop-order'
        str_to_sign = str(now) + 'POST' + '/api/v1/stop-order' + data_json
    else:
        url = 'https://api-futures.kucoin.com/api/v1/orders'
        str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        'Content-Type': 'application/json'
    }
    response = requests.request('post', url, headers=headers, data=data_json)
    return response.json()


def get_futures_completed_orders(api_key, api_secret, api_passphrase):
    now = int(time.time() * 1000)
    url = 'https://api-futures.kucoin.com/api/v1/recentDoneOrders'
    str_to_sign = str(now) + 'GET' + '/api/v1/recentDoneOrders'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        'Content-Type': 'application/json'
    }
    response = requests.request('get', url, headers=headers)
    return response.json()['data']


def create_order(order_type, api_key, api_secret, api_passphrase, **payload):
    payload['clientOid'] = randint(1, 10000) * 1000
    now = int(time.time() * 1000)
    data_json = json.dumps(payload)
    if order_type == 's':
        url = 'https://api.kucoin.com/api/v1/orders'
        str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
    else:
        url = 'https://api-futures.kucoin.com/api/v1/orders'
        str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        'Content-Type': 'application/json'
    }
    response = requests.request('post', url, headers=headers, data=data_json)
    return response.json()


def cancel_all_orders(order_type, api_key, api_secret, api_passphrase):
    now = int(time.time() * 1000)
    if order_type == 's':
        url = 'https://api.kucoin.com/api/v1/stop-order/cancel'
        str_to_sign = str(now) + 'DELETE' + '/api/v1/stop-order/cancel'
    else:
        url = 'https://api-futures.kucoin.com/api/v1/orders'
        str_to_sign = str(now) + 'DELETE' + '/api/v1/orders'

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        'Content-Type': 'application/json'
    }
    response = requests.request('delete', url, headers=headers)
    return response.json()


def get_cryptocurrency_price(order_type, symbol, api_key, api_secret, api_passphrase):
    now = int(time.time() * 1000)
    if order_type == 's':
        url = f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}'
        str_to_sign = str(now) + 'GET' + \
            f'/api/v1/market/orderbook/level1?symbol={symbol}'
    else:
        url = f'https://api-futures.kucoin.com/api/v1/ticker?symbol={symbol}'
        str_to_sign = str(now) + 'GET' + f'/api/v1/ticker?symbol={symbol}'

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        'Content-Type': 'application/json'
    }
    response = requests.request('get', url, headers=headers)
    return response.json()['data']['price']

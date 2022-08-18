from datetime import timedelta
from transaction.models import Transaction

from django.utils import timezone
from utilities import diff_between_two_dates, send_sms

def check_user_special_account():
    transactions = Transaction.objects.filter(is_confirmation=True)
    for transaction in transactions:
        result = diff_between_two_dates(transaction.date_of_approval + timedelta(transaction.validity_rate + 1), timezone.now()).days
        if result == 10:
            send_sms('np5tviaoag', str(transaction.user.phone_number), {'date_cnt': str(result)})
        elif result == 5:
            send_sms('np5tviaoag', str(transaction.user.phone_number), {'date_cnt': str(result)})
        elif result == 3:
            send_sms('np5tviaoag', str(transaction.user.phone_number), {'date_cnt': str(result)})
        elif result == 1:
            send_sms('np5tviaoag', str(transaction.user.phone_number), {'date_cnt': str(result)})
        elif result <= 0:
            send_sms('3egblee8ys', str(transaction.user.phone_number), {'name': transaction.user.full_name.split()[0]})
            transaction.delete()


def check_user_transaction_status():
    transactions = Transaction.objects.filter(is_send_receipt=True, is_confirmation=False)
    for transaction in transactions:
        # minutes
        result = diff_between_two_dates(timezone.now(), transaction.last_updated_time).seconds / 60
        if result >= 3 and transaction.transaction_status !='در صف ورود' and transaction.transaction_status != 'ارسال به مرکز کنترل':
            transaction.transaction_status = 'در صف ورود'
            transaction.save()
        elif result >= 5 and transaction.transaction_status == 'در صف ورود':
            transaction.transaction_status = 'ارسال به مرکز کنترل'
            transaction.save()
        elif result >= 30:
            transaction.transaction_status = 'در حال بررسی'
            transaction.save()
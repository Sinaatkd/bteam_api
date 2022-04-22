from datetime import timedelta
from django.utils import timezone
from utilities import diff_between_two_dates, send_sms
from transaction.models import Transaction
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        transactions = Transaction.objects.filter(is_confirmation=True)
        for transaction in transactions:
            result = diff_between_two_dates(transaction.date_of_approval + timedelta(transaction.validity_rate + 1), timezone.now()).days
            print(result)
            print(transaction.user.phone_number)
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
            
            self.stdout.write(self.style.SUCCESS(f'Checked Transaction "{transaction}"'))
from django.utils import timezone
from utilities import diff_between_two_dates
from transaction.models import Transaction
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        transactions = Transaction.objects.filter(is_send_receipt=True, is_confirmation=False)
        for transaction in transactions:
            # minutes
            result = diff_between_two_dates(timezone.now(), transaction.last_updated_time).seconds / 60
            print(result)
            if result >= 3 and transaction.transaction_status !='در صف ورود' and transaction.transaction_status != 'ارسال به مرکز کنترل':
                transaction.transaction_status = 'در صف ورود'
                transaction.save()
            elif result >= 5 and transaction.transaction_status == 'در صف ورود':
                transaction.transaction_status = 'ارسال به مرکز کنترل'
                transaction.save()
            elif result >= 30:
                transaction.transaction_status = 'در حال بررسی'
                transaction.save()
            self.stdout.write(self.style.SUCCESS(f'Checked Transaction id "{transaction.id}"'))
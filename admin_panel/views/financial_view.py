from datetime import timedelta
from django.shortcuts import render
from django.db.models import Sum
from admin_panel.decorators import check_group
from account.models import User
from transaction.models import Transaction

import jdatetime


@check_group('مالی')
def finanical_statistics(request):
    date_values = request.GET.get('date', None)
    year, month, day = 1, 1, 1
    if date_values is not None and date_values != '':
        year, month, day = date_values.split('/')
    date = jdatetime.datetime(year=int(year), month=int(month), day=int(day)).togregorian()
    users = User.objects.all()
    if date_values is not None and date_values != '':
        all_transactions = Transaction.objects.filter(is_confirmation=True, last_updated_time__range=[date, date + timedelta(days=1)])
    else:
        all_transactions = Transaction.objects.filter(is_confirmation=True,)
    sum_transaction = all_transactions.aggregate(Sum('amount'))['amount__sum']
    context = {'all_transactions': all_transactions.count(
    ), 'sum_transactions_amount': sum_transaction, 'data': []}
    for user in users:
        if date_values is not None and date_values != '':
            transactions = Transaction.objects.filter(
                consultant_name=user.id, is_confirmation=True, last_updated_time__range=[date, date + timedelta(days=1)])
        else:
            transactions = Transaction.objects.filter(consultant_name=user.id, is_confirmation=True,)
        if transactions.count() > 0:
            transactions_count = transactions.count()
            transactions_sum_amount = transactions.aggregate(Sum('amount'))[
                'amount__sum']
            new_data = {'id': user.id, 'full_name': user.full_name,
                        'count': transactions_count, 'amount_sum': transactions_sum_amount, 'wallet': user.wallet, 'transactions': transactions}
            context['data'].append(new_data)

    return render(request, 'financial/financial_view.html', context)

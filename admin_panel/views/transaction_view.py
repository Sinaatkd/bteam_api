from datetime import timedelta
from django.utils.timezone import now
from admin_panel.decorators import check_group
from utilities import send_sms
from account.models import User, UserGift
from django.utils.timezone import now
from django.shortcuts import redirect
from django.views.generic import ListView
from transaction.models import DiscountCode, Transaction
from utilities import generate_unique_gift_code

@check_group('دسترسی به کاربران')
def confirm_transaction(request, transaction_id):
    selected_transaction = Transaction.objects.get(id=transaction_id)
    if selected_transaction.transaction_status in ['در حال بررسی' ,'تایید شده', 'رد شده']:
        selected_transaction.transaction_status = 'تایید شده'
        selected_transaction.date_of_approval = now()
        selected_transaction.is_confirmation = True
        selected_transaction.is_send_receipt = True
        try:
            if selected_transaction.amount > 0:
                user = User.objects.filter(id=int(selected_transaction.consultant_name)).first()
                if user is not None:
                # It was commented because when the transaction is deleted, the prize is also deleted
                    user_gift = UserGift.objects.create(code=generate_unique_gift_code(), gift_type='black-b', user=user,for_what='buy', transaction=selected_transaction)
                    send_sms('iv0noup6wjdomqi', user.phone_number, {'bname': user.full_name.split()[0], 'cartname': user_gift.gift_type})
                    # UserGift.objects.create(code=generate_unique_gift_code(), gift_type='black-b', user=user,for_what='buy')
                # UserGift.objects.create(code=generate_unique_gift_code(), gift_type='red-b', user=selected_transaction.user,for_what='buy')

        except:
            pass
        if selected_transaction.amount > 0:
            user_gift = UserGift.objects.create(code=generate_unique_gift_code(), gift_type='red-b', user=selected_transaction.user,for_what='buy', transaction=selected_transaction)
            send_sms('iv0noup6wjdomqi', selected_transaction.user.phone_number, {'bname': selected_transaction.user.full_name.split()[0], 'cartname': user_gift.gift_type})

        selected_transaction.save()
        send_sms('ienj1gpm8e', selected_transaction.user.phone_number, {'name': str(selected_transaction.user.full_name).split()[0]})
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def unconfirm_transaction(request, transaction_id):
    if request.method == 'POST':
        selected_transaction = Transaction.objects.get(id=transaction_id)
        if selected_transaction.transaction_status in ['در حال بررسی' ,'تایید شده', 'رد شده']:
            selected_transaction.transaction_status = 'رد شده'
            send_sms('cwjltta64a', selected_transaction.user.phone_number, {'reject': request.POST.get('reject_text')})
            selected_transaction.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def deactive_discount_code(request, discount_code_id):
    selected_discount_code = DiscountCode.objects.get(id=discount_code_id)
    selected_discount_code.is_active = False
    selected_discount_code.save()
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def active_discount_code(request, discount_code_id):
    selected_discount_code = DiscountCode.objects.get(id=discount_code_id)
    selected_discount_code.is_active = True
    selected_discount_code.save()
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def set_private_discount(request, discount_code_id):
    selected_discount_code = DiscountCode.objects.get(id=discount_code_id)
    selected_discount_code.is_private = True
    selected_discount_code.save()
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def set_public_discount(request, discount_code_id):
    selected_discount_code = DiscountCode.objects.get(id=discount_code_id)
    selected_discount_code.is_private = False
    selected_discount_code.save()
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def add_discount_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        count = request.POST.get('count')
        is_private = request.POST.get('is_private')
        if is_private is not None:
            is_private = True
        else:
            is_private = False
        percentage = request.POST.get('percentage')
        valid_days = request.POST.get('valid_days')
        DiscountCode.objects.create(code=code, count=count, percentage=percentage, validity_date=now() + timedelta(int(valid_days)), is_private=is_private)

    return redirect(request.META.get('HTTP_REFERER'))

class TransactionsList(ListView):
    queryset = Transaction.objects.filter(is_confirmation=False).order_by('-id')
    template_name = 'transactions/transactions_list.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionsList, self).get_context_data(**kwargs)
        context['unconfirmed_transactions'] = Transaction.objects.filter(is_confirmation=True).order_by('-id')
        return context

class DiscountCodesList(ListView):
    queryset = DiscountCode.objects.all().order_by('-is_active')
    template_name = 'transactions/discount_codes_list.html'
    paginate_by = 20
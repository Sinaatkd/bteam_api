from django.shortcuts import redirect
from django.views.generic.list import ListView
from account.models import UserCashWithdrawal
from admin_panel.decorators import check_group
from utilities import send_sms


@check_group('مالی')
def confirm_cash_withdrawal(request, id):
    if request.method == 'POST':
        paycode = request.POST.get('paycode', None) 

        cashWithdrawal = UserCashWithdrawal.objects.filter(id=id).first()
        cashWithdrawal.is_confirmation = True
        cashWithdrawal.paycode = paycode
        cashWithdrawal.save()
        send_sms('vq1dmgvux4u038n', cashWithdrawal.user.phone_number, {'fname': cashWithdrawal.user.full_name.split()[0], 'varizi': str(cashWithdrawal.amount), 'peycode': str(paycode)})
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('مالی')
def delete_cash_withdrawal(request, id):
    cashWithdrawal = UserCashWithdrawal.objects.filter(id=id).first()
    cashWithdrawal.delete()
    return redirect(request.META.get('HTTP_REFERER'))

class CashWithdrawalList(ListView):
    queryset = UserCashWithdrawal.objects.all().order_by('is_confirmation')
    template_name = 'cash_withdrawal/cash_withdrawal_list.html'
    paginate_by = 20
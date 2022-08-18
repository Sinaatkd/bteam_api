from django.urls import reverse

from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from account.models import Device, User, UserMessage
from admin_panel.decorators import check_group
from admin_panel.forms import EditUserForm
from signals.models import SpotSignal, FuturesSignal
from news.models import News
from transaction.models import Transaction
from special_account_item.models import SpecialAccountItem

from utilities import send_sms, send_sms_without_pattern


# Create your views here.
def home_page(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if request.POST.get('for') == 'all':
            phone_numbers = [f'98{phone_number.get("phone_number")}' for phone_number in User.objects.all().values('phone_number')]
            send_sms_without_pattern(text, phone_numbers)
        elif request.POST.get('for') == 'has-transaction':
            phone_numbers = [f'98{phone_number.user.phone_number}' for phone_number in Transaction.objects.all()]
            send_sms_without_pattern(text, phone_numbers)
        elif request.POST.get('for') == 'no-transaction':
            phone_numbers = [f'98{phone_number.get("phone_number")}' for phone_number in User.objects.filter(transaction=None).values('phone_number')]
            send_sms_without_pattern(text, phone_numbers)



    latest_user = User.objects.all().order_by('-id')[:10]
    users_count = User.objects.all().count()
    signals_count = SpotSignal.objects.all().count() + FuturesSignal.objects.all().count()
    news_count = News.objects.all().count()
    special_accounts_count =  SpecialAccountItem.objects.all().count()
    context = {
        'latest_user': latest_user,
        'users_count': users_count,
        'signals_count': signals_count,
        'news_count': news_count,
        'special_accounts_count': special_accounts_count,
    }
    return render(request, 'home_page.html', context)

@check_group('دسترسی به کاربران')
def user_edit(request, pk):
    selected_user = User.objects.filter(id=pk).first()
    user_messages = UserMessage.objects.filter(user=selected_user)
    user_messages = UserMessage.objects.filter(user=selected_user)
    user_transaction = Transaction.objects.filter(user=selected_user).first()
    groups = Group.objects.all()
    edit_form = EditUserForm(request.POST or None, initial={
                             'username': selected_user.username, 
                             'phone_number': selected_user.phone_number, 
                             'full_name': selected_user.full_name,
                             'national_code': selected_user.national_code,
                             'from_city': selected_user.from_city,
                             'wallet': selected_user.wallet,
                             'is_staff': selected_user.is_staff})

    if edit_form.is_valid():
        username = edit_form.cleaned_data.get('username')
        full_name = edit_form.cleaned_data.get('full_name')
        from_city = edit_form.cleaned_data.get('from_city')
        national_code = edit_form.cleaned_data.get('national_code')
        phone_number = edit_form.cleaned_data.get('phone_number')
        is_staff = edit_form.cleaned_data.get('is_staff')
        wallet = edit_form.cleaned_data.get('wallet')

        selected_user.username = username
        selected_user.from_city = from_city
        selected_user.national_code = national_code
        selected_user.full_name = full_name
        selected_user.phone_number = phone_number
        selected_user.is_staff = is_staff
        selected_user.wallet = wallet
        selected_user.save()

    context = {
        'selected_user': selected_user,
        'user_messages': user_messages,
        'user_messages': user_messages,
        'edit_form': edit_form,
        'user_transaction': user_transaction,
        'groups': groups
    }
    return render(request, 'users/user_edit.html', context)


@check_group('دسترسی به کاربران')
def set_user_permission(request, user_id):
    selected_user = User.objects.get(id=user_id)
    if request.method == 'POST':
        selected_user.groups.clear()
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                group = Group.objects.get(name=data)
                selected_user.groups.add(group)
                selected_user.save()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.device.delete()
    user.delete()
    return redirect(reverse('users_list'))

@check_group('دسترسی به کاربران')
def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def unconfirm_full_auth(request, user_id):
    reject = request.POST.get('reject_text')
    user = User.objects.get(id=user_id)
    user.father_name = None
    user.father_name = None
    user.place_of_issue = None
    user.date_of_birth = None
    user.id_card = None
    user.face = None
    user.save()
    send_sms('8hvg5dw0mz1651p', user.phone_number, {'reject': reject})
    return redirect(request.META.get('HTTP_REFERER'))



@check_group('دسترسی به کاربران')
def confirm_full_auth(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_full_authentication = True
    user.save()
    send_sms('iqne6lhel7u25k2', user.phone_number ,{'firstname': user.full_name.split()[0] })
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect(request.META.get('HTTP_REFERER'))


@check_group('دسترسی به کاربران')
def remove_device_uuid(request, device_id):
    selected_device = Device.objects.get(id=device_id)
    selected_device.uuid = None
    selected_device.save()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def add_user_message(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
        UserMessage.objects.create(title=title, description=description, user_id=user_id)
    return redirect(request.META.get('HTTP_REFERER'))



class UsersList(ListView):
    template_name = 'users/users_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all().order_by('-id')
        s = self.request.GET.get('s')
        if s is not None:
            queryset = User.objects.filter(full_name__icontains=s).order_by('-id')
        return queryset


class UsersFullAuthList(ListView):
    template_name = 'users/users_list.html'

    def get_queryset(self):
        queryset = User.objects.filter(father_name__isnull=False, is_full_authentication=False).order_by('-id')
        print(queryset)
        s = self.request.GET.get('s')
        if s is not None:
            queryset = User.objects.filter(father_name__isnull=False, full_name__icontains=s, is_full_authentication=False).order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        confirmed_users = User.objects.filter(father_name__isnull=False, is_full_authentication=True).order_by('-id')
        s = self.request.GET.get('s')
        if s is not None:
            confirmed_users = User.objects.filter(father_name__isnull=False, full_name__icontains=s, is_full_authentication=True).order_by('-id')
        context = {
            'confirmed_users': confirmed_users
        }
        return super().get_context_data(**kwargs, **context)
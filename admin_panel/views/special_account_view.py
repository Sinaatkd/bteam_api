from django.shortcuts import redirect

from django.views.generic import ListView
from admin_panel.decorators import check_group
from special_account_item.models import SpecialAccountItem

class SpecialAccountItemList(ListView):
    queryset = SpecialAccountItem.objects.all().order_by('-id')
    template_name = 'special_account/special_account_list.html'
    paginate_by = 20


@check_group('دسترسی به کاربران')
def delete_special_account(request, special_account_id):
    news = SpecialAccountItem.objects.get(id=special_account_id)
    news.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def add_special_account(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        expire_day = request.POST.get('expire_day')
        price = request.POST.get('price')
        SpecialAccountItem.objects.create(title=title, expire_day=expire_day, price=price)

    return redirect(request.META.get('HTTP_REFERER'))

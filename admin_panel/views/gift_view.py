from django.views.generic import ListView
from django.shortcuts import redirect, render
from account.models import User, UserGift, UserGiftLog
from admin_panel.decorators import check_group
from utilities import generate_unique_gift_code

def add_gift(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        for_what = request.POST.get('for_what', None)
        gift_type = request.POST.get('gift_type', None)
        UserGift.objects.create(user_id=user_id, for_what=for_what, gift_type=gift_type, code=generate_unique_gift_code())
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def deactive_user_gift(request, gift_id):
    gift = UserGift.objects.filter(id=gift_id).first()
    gift.is_active = False
    gift.save()    
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def active_user_gift(request, gift_id):
    gift = UserGift.objects.filter(id=gift_id).first()
    gift.is_active = True
    gift.save()    
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به کاربران')
def user_gifts_detail(request, user_id):
    gifts = UserGift.objects.filter(user_id=user_id)
    gift_logs = UserGiftLog.objects.filter(user_id=user_id)
    context = {
        'gifts': gifts,
        'user_id': user_id,
        'gift_logs': gift_logs,
    }
    return render(request, 'gifts/user_gifts_detail.html', context)


class UsersList(ListView):
    template_name = 'gifts/users_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all().order_by('-id')
        s = self.request.GET.get('s')
        if s is not None:
            queryset = User.objects.filter(full_name__icontains=s).order_by('-id')
        return queryset
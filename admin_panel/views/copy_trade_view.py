from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView
from admin_panel.forms import BasketForm
from copy_trade.models import Basket


class BasketsList(ListView):
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='تریدر').exists() or self.request.user.groups.filter(name='مدیر').exists():
            baskets = Basket.objects.filter(trader=self.request.user).order_by('-is_active', '-id')
        return baskets


class CreateBasket(CreateView):
    model = Basket
    form_class = BasketForm
    # success_url = reverse('baskets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.trader = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('baskets'))
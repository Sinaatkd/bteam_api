from random import randint
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from admin_panel.forms import BasketForm, StageForm
from copy_trade.models import Basket, Stage
from utilities import create_futures_order, create_order, get_active_orders


class BasketsList(ListView):
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='تریدر').exists() or self.request.user.groups.filter(name='مدیر').exists():
            baskets = Basket.objects.filter(trader=self.request.user).order_by('-is_active', '-id')
        return baskets


class CreateBasket(CreateView):
    model = Basket
    form_class = BasketForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.trader = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('baskets'))


class DetailBasket(DetailView):
    model = Basket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stage_form'] = StageForm(self.request.POST or None)
        return context
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        data = request.POST
        selected_basket = Basket.objects.get(pk=pk)
        new_stage = Stage.objects.create(title=data.get('title'), amount=data.get('amount'))
        selected_basket.stages.add(new_stage)
        return HttpResponseRedirect(reverse('detail_basket', kwargs={'pk': pk}))


def delete_basket(request, pk):
    selected_basket = Basket.objects.get(pk=pk)
    selected_basket.delete()
    return HttpResponseRedirect(reverse('baskets'))


def disabled_accept_participant(request, pk):
    selected_basket = Basket.objects.get(pk=pk)
    selected_basket.is_accept_participant = False
    selected_basket.save()
    return HttpResponseRedirect(reverse('detail_basket', kwargs={'pk': pk}))

def apply_order_for_participants(request, pk):
    basket = Basket.objects.get(pk=pk)
    if basket.orders_type == 's':
        trader_active_orders = get_active_orders('s', basket.trader_spot_api, basket.trader_spot_secret, basket.trader_spot_passphrase)
        for order in trader_active_orders:
            symbol = order['symbol']
            size = float(order['size'])
            side = order['side']
            price = float(order['price'])
            stop_price = float(order['stopPrice'])
            for participant in basket.participants.all():
                api_key = participant.user_kucoin_api.spot_api_key
                api_secret = participant.user_kucoin_api.spot_secret
                api_passphrase = participant.user_kucoin_api.spot_passphrase
                create_order(api_key, api_secret, api_passphrase, symbol, size, side, price, stop_price)
    elif basket.orders_type == 'f':
        trader_active_orders = get_active_orders('f', basket.trader_futures_api, basket.trader_futures_secret, basket.trader_futures_passphrase)
        for order in trader_active_orders:
            print(order)
            symbol = order['symbol']
            size = float(order['size'])
            side = order['side']
            price = float(order['price'])
            stop_price = float(order['stopPrice'])
            stop_price_type = order['stopPriceType']
            leverage = float(order['leverage'])
            print(symbol, size, side, price, stop_price, leverage)
            for participant in basket.participants.all():
                api_key = participant.user_kucoin_api.futures_api_key
                api_secret = participant.user_kucoin_api.futures_secret
                api_passphrase = participant.user_kucoin_api.futures_passphrase
                new_order = create_futures_order(side, symbol, stop_price, size, price, stop_price_type, leverage, api_key, api_secret, api_passphrase)
                print(new_order)

    return HttpResponseRedirect(reverse('detail_basket', kwargs={'pk': pk}))
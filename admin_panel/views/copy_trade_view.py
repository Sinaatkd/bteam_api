from random import randint
import threading
from datetime import datetime, timedelta
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from admin_panel.forms import BasketForm, StageForm
from copy_trade.models import Basket, Order, Stage
from utilities import create_order, get_active_orders


class BasketsList(ListView):
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='دسترسی به کپی ترید').exists() or request.user.groups.filter(name='مدیر').exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404

    def get_queryset(self):
        return Basket.objects.filter(trader=self.request.user).order_by('-is_active', '-id')


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
        new_stage = Stage.objects.create(
            title=data.get('title'), amount=data.get('amount'))
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


def apply_order_for_participants_thread(basket):
    api_key = basket.trader_spot_api if basket.orders_type == 's' else basket.trader_futures_api
    secret_key = basket.trader_spot_secret if basket.orders_type == 's' else basket.trader_futures_secret
    passphrase = basket.trader_spot_passphrase if basket.orders_type == 's' else basket.trader_futures_passphrase
    trader_active_orders = get_active_orders(
        basket.orders_type, api_key, secret_key, passphrase)
    for order in trader_active_orders:
        order_created_time = order.get('createdAt')
        five_minute_ago_timestamp =  (datetime.now() - timedelta(minutes=5)).timestamp()

        if order_created_time > five_minute_ago_timestamp:
            paylaod = {
                'symbol': order.get('symbol', None),
                'size': float(order.get('size', None)) if order.get('size', None) != None else order.get('size', None),
                'side': order.get('side', None),
                'price': float(order.get('price', None)) if order.get('price', None) != None else order.get('price', None),
                'stopPrice': float(order.get('stopPrice', None)),
                'stopPriceType': order.get('stopPriceType', None),
                'leverage': order.get('leverage', None),
                'type': order.get('type', None),
            }

            paylaod['order_type'] = paylaod['type']
            del paylaod['type']

            basket_new_order = Order.objects.create(**paylaod)
            basket.orders.add(basket_new_order)

            paylaod['type'] = paylaod['order_type']
            stop = order.get('stop', None)
            paylaod['stop'] = stop
            del paylaod['order_type']

            
            for participant in basket.participants.all():
                participant_api = participant.user_kucoin_api
                api_key = participant_api.spot_api_key if basket.orders_type == 's' else participant_api.futures_api_key
                api_secret = participant_api.spot_secret if basket.orders_type == 's' else participant_api.futures_secret
                api_passphrase = participant_api.spot_passphrase if basket.orders_type == 's' else participant_api.futures_passphrase
                create_order(basket.orders_type, api_key, api_secret,
                            api_passphrase, **paylaod)

def apply_order_for_participants(request, pk):
    basket = Basket.objects.get(pk=pk)
    thread = threading.Thread(
        target=apply_order_for_participants_thread, kwargs={'basket': basket})
    thread.start()
    return HttpResponseRedirect(reverse('detail_basket', kwargs={'pk': pk}))


def set_stage(request, pk):
    stage = Stage.objects.get(pk=pk)
    if not stage.is_pay_time:
        stage.is_pay_time = True
        stage.save()
        basket = Basket.objects.filter(stages__in=[stage]).first()
        basket.is_freeze = True
        basket.save()
    return redirect(request.META.get('HTTP_REFERER'))

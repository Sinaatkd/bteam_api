from django.shortcuts import redirect, render, resolve_url
from django.views.generic import ListView
from admin_panel.decorators import check_group
from utilities import send_notification

from signals.models import FuturesSignal, SignalNews, Target

class FuturesSignalsList(ListView):
    queryset = FuturesSignal.objects.all().order_by('-id')
    template_name = 'futures_signals/futures_signals_list.html'
    paginate_by = 20

@check_group('دسترسی به سیگنال')
def detail_futures(request, futures_id):
    selected_futures = FuturesSignal.objects.get(id=futures_id)
    
    context = {
        'selected_futures': selected_futures
    }

    return render(request, 'futures_signals/futures_detail.html', context)


@check_group('دسترسی به سیگنال')
def close_futures_signal(request, futures_id):
    if request.method == 'POST':
        selected_futures = FuturesSignal.objects.get(id=futures_id)
        selected_futures.is_active = False
        selected_futures.profit_of_signal_amount = float(request.POST.get('profit_of_signal_amount'))
        selected_futures.status = request.POST.get('status')
        selected_futures.save()
        send_notification(f'سیگنال {selected_futures.coin_symbol}', 'بسته شد')
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به سیگنال')
def delete_futures_signal(request, futures_id):
    selected_futures = FuturesSignal.objects.get(id=futures_id)
    selected_futures.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به سیگنال')
def add_futures_target(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        futures_id = int(request.POST.get('futures_id'))
        selected_futures = FuturesSignal.objects.get(id=futures_id)
        selected_futures.targets.add(Target.objects.create(title=title, amount=amount))
    return redirect(request.META.get('HTTP_REFERER'))
    
@check_group('دسترسی به سیگنال')
def add_futures_news(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        futures_id = int(request.POST.get('futures_id'))
        selected_futures = FuturesSignal.objects.get(id=futures_id)
        selected_futures.signal_news.add(SignalNews.objects.create(content=content))
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به سیگنال')
def add_futures_signal(request):
    if request.method == 'POST':
        coin_symbol = request.POST.get('coin_symbol')
        amount = int(request.POST.get('amount'))
        leverage = int(request.POST.get('leverage'))
        type_of_investment = request.POST.get('type_of_investment')
        stop_loss = request.POST.get('stop_loss')
        entry = request.POST.get('entry')
        futures= FuturesSignal.objects.create(coin_symbol=coin_symbol, amount=amount, leverage=leverage, type_of_investment=type_of_investment, stop_loss=stop_loss, entry=entry)
        send_notification(f'سیگنال {coin_symbol}', 'در انتظار ورود')
        return redirect(resolve_url('detail_futures', futures_id=futures.id))
    return render(request, 'futures_signals/add_futures.html')
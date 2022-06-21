from django.shortcuts import redirect, render, resolve_url
from django.views.generic import ListView
from admin_panel.decorators import check_group
from utilities import send_notification

from signals.models import SignalAlarm, SpotSignal, SignalNews, Target

class SpotSignalsList(ListView):
    queryset = SpotSignal.objects.all().order_by('-id')
    template_name = 'spot_signals/spot_signals_list.html'
    paginate_by = 20

@check_group('دسترسی به سیگنال')
def detail_spot(request, spot_id):
    selected_spot = SpotSignal.objects.get(id=spot_id)
    
    context = {
        'selected_spot': selected_spot
    }

    return render(request, 'spot_signals/spot_detail.html', context)


@check_group('دسترسی به سیگنال')
def add_spot_alarm(request):
    if request.method == 'POST':
        spot_id = request.POST.get('spot_id')
        title = request.POST.get('title')
        selected_spot = SpotSignal.objects.get(id=spot_id)
        selected_spot.alarms.add(SignalAlarm.objects.create(title=title))
        send_notification(title=f'سیگنال {selected_spot.coin_symbol}', content=title, is_send_sms=False)
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به سیگنال')
def delete_spot_signal(request, spot_id):
    selected_spot = SpotSignal.objects.get(id=spot_id)
    selected_spot.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به سیگنال')
def close_spot_signal(request, spot_id):
    if request.method == 'POST':
        selected_spot = SpotSignal.objects.get(id=spot_id)
        selected_spot.is_active = False
        selected_spot.profit_of_signal_amount = float(request.POST.get('profit_of_signal_amount'))
        selected_spot.status = request.POST.get('status')
        selected_spot.save()
        send_notification(f'سیگنال {selected_spot.coin_symbol}', 'بسته شد')
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به سیگنال')
def add_spot_target(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        spot_id = int(request.POST.get('spot_id'))
        selected_spot = SpotSignal.objects.get(id=spot_id)
        selected_spot.targets.add(Target.objects.create(title=title, amount=amount))
    return redirect(request.META.get('HTTP_REFERER'))
    
@check_group('دسترسی به سیگنال')
def add_spot_news(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        spot_id = int(request.POST.get('spot_id'))
        selected_spot = SpotSignal.objects.get(id=spot_id)
        selected_spot.signal_news.add(SignalNews.objects.create(content=content))
    return redirect(request.META.get('HTTP_REFERER'))
    
@check_group('دسترسی به سیگنال')
def add_spot_signal(request):
    if request.method == 'POST':
        coin_symbol = request.POST.get('coin_symbol')
        proposed_capital = int(request.POST.get('proposed_capital'))
        r_and_r = float(request.POST.get('r_and_r'))
        type_of_investment = request.POST.get('type_of_investment')
        stop_loss = request.POST.get('stop_loss')
        entry = request.POST.get('entry')
        signal = SpotSignal.objects.create(coin_symbol=coin_symbol, proposed_capital=proposed_capital, r_and_r=r_and_r, type_of_investment=type_of_investment, stop_loss=stop_loss, entry=entry)
        send_notification(f'سیگنال {coin_symbol}', 'در انتظار ورود')
        return redirect(resolve_url('detail_spot', spot_id=signal.id))
    return render(request, 'spot_signals/add_spot.html')

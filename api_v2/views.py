import time
import hashlib
import base64
import hmac
import requests
from math import ceil
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.core.files.base import ContentFile
from django.db.models import Sum
from rest_framework.generics import CreateAPIView
from banner.models import Banner
from copy_trade.models import Basket
from signals.models import FuturesSignal, SignalAlarm, SpotSignal, Target


from utilities import calculate_profit_of_signals, check_user_usdt_balance, diff_between_two_dates, generate_token, get_now_jalali_date, get_prev_touched_target, get_random_string, is_first_target_touched, send_notification, send_sms, send_verification_code

import rest_framework.status as status_code
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAccountOwner, IsTransactionOwner
from .serializer import (BannerSerializer, BasketSerializer, CheckDiscountCodeSerializer, DiscountCodeSerializer, FuturesSignalSerializer,
                         SpecialAccountItemSerializer, SpotSignalSerializer,
                         TransactionSerializer, UserCashWithdrawalSerializer, UserGiftLogSerializer,
                         UserLoginVerificationCodeSerializer,
                         UserLoginWithPasswordSerializer, UserMessageSerializer,
                         UserRegisterSerializer,
                         UserSerializer)
from account.models import User, UserCashWithdrawal, UserGift, UserGiftLog, UserKucoinAPI, UserMessage, VerificationCode
from special_account_item.models import SpecialAccountItem
from transaction.models import DiscountCode, Transaction


class RegisterUserAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)


class SendVerificationCodeAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        send_verification_code(request.data.get('phone_number', ''))
        return Response({'message': 'sent'}, status=status_code.HTTP_200_OK)


class ForgotPassAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        new_pass = request.data.get('new_pass')
        verification_code = VerificationCode.objects.filter(
            code=request.data.get('verification_code')).last()
        if not verification_code.is_expire:
            user = User.objects.filter(phone_number=phone_number).first()
            user.set_password(new_pass)
            user.save()
            return Response({'message': 'ok'}, status=status_code.HTTP_200_OK)

        return Response({'message': 'code is expired'}, status=status_code.HTTP_400_BAD_REQUEST)


class LoginUserWithVerificationCodeAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        auth_serializer = UserLoginVerificationCodeSerializer(
            data=request.data, context={'request': request})
        if auth_serializer.is_valid():
            request.user.is_phone_number_verified = True
            request.user.save()
            token = generate_token(request.user)
            return Response({'token': token.key}, status=status_code.HTTP_200_OK)
        return Response(auth_serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)


class LoginUserWithUserPassAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginWithPasswordSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({'token': generate_token(self.request.user).key})
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)


class GetSpecialAccountItemListAPI(ListAPIView):
    queryset = SpecialAccountItem.objects.filter(is_active=True)
    serializer_class = SpecialAccountItemSerializer


class GetUserInfoAPI(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user, many=False)
        transaction = Transaction.objects.filter(user=request.user).first()
        unread_messages = UserMessage.objects.filter(
            user=request.user, is_seen=False).count()
        if transaction is not None:
            special_item_title = transaction.special_item.title
            transaction = TransactionSerializer(transaction).data
            transaction['special_item'] = special_item_title
        result = {
            'user': serializer.data,
            'transaction': transaction,
            'unread_messages': unread_messages
        }
        return Response(result, status=status_code.HTTP_200_OK)


class GetUserMessages(ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user).order_by('is_seen')


class SeenAllUserMessage(APIView):
    def get(self, request):
        user_messages = UserMessage.objects.filter(
            user=self.request.user, is_seen=False)
        for message in user_messages:
            message.is_seen = True
            message.save()
        return Response({'message': 'ok'}, 200)


class EditUserAPI(UpdateAPIView):
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('id_card'):
            try:
                format, imgstr = request.data.get('id_card').split(';base64,')
                ext = format.split('/')[-1]
                id_card = ContentFile(
                    base64.b64decode(imgstr), name='temp.' + ext)
                instance.id_card = id_card
            except:
                pass
            del request.data['id_card']
        if request.data.get('face'):
            try:
                format, imgstr = request.data.get('face').split(';base64,')
                ext = format.split('/')[-1]
                face = ContentFile(
                    base64.b64decode(imgstr), name='temp.' + ext)
                instance.face = face
            except:
                pass
            del request.data['face']
        instance.save()
        return super().put(request, *args, **kwargs)


class CreateTransactionAPI(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)


class CancelTransactionAPI(APIView):
    def get(self, request):
        transaction = Transaction.objects.filter(user=request.user).first()
        transaction.delete()
        return Response({'message': 'ok'}, 200)


class CheckDiscountCodeAPI(APIView):
    def post(self, request):
        check_discount_code_serializer = CheckDiscountCodeSerializer(
            data=request.data,  context={'request': request})
        if check_discount_code_serializer.is_valid():
            amount = float(request.data.get('amount', None))
            request.discount_code.use_by.add(request.user)
            new_amount = (request.discount_code.percentage * int(amount)) / 100
            return Response({'status': 'ok', 'discount_code_id': request.discount_code.id, 'new_amount': amount - new_amount}, status=status_code.HTTP_200_OK)
        return Response(check_discount_code_serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)


class SendReceiptImageAPI(RetrieveUpdateAPIView):
    permission_classes = [IsTransactionOwner]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        format, imgstr = request.data.get('payment_receipt').split(';base64,')
        ext = format.split('/')[-1]
        payment_receipt = ContentFile(
            base64.b64decode(imgstr), name='temp.' + ext)
        instance.payment_receipt = payment_receipt
        instance.is_send_receipt = True
        instance.transaction_status = 'درحال پردازش'
        instance.last_updated_time = now()
        instance.save()
        send_sms('hkdf6b6rwr', self.request.user.phone_number, {
                 "name": self.request.user.full_name.split()[0]})

        return Response({'message': 'ok'}, status=status_code.HTTP_200_OK)


class GetAllPublicDiscountAPI(ListAPIView):
    queryset = DiscountCode.objects.filter(
        is_active=True, count__gt=0, is_private=False)
    serializer_class = DiscountCodeSerializer


class GetAllActiveFuturesSignals(ListAPIView):
    queryset = FuturesSignal.objects.filter(is_active=True)
    serializer_class = FuturesSignalSerializer


class GetAllActiveSpotSignals(ListAPIView):
    queryset = SpotSignal.objects.filter(is_active=True)
    serializer_class = SpotSignalSerializer


class GetAllDeactiveSignals(APIView):
    def get(self, request):
        type_of_filter = request.query_params.get('range', 'daily')
        days = 1
        today = datetime.today()
        if type_of_filter == 'daily':
            days = 1
        elif type_of_filter == 'weekly':
            days = 7
        elif type_of_filter == 'monthly':
            days = 30

        range_date = today - timedelta(days=days)
        deactives_futures_signals = FuturesSignal.objects.filter(
            is_active=False, created_time__range=[range_date, today]).order_by('-id')
            
        deactives_spot_signals = SpotSignal.objects.filter(
            is_active=False, created_time__range=[range_date, today]).order_by('-id')
            
        closed_with_profit_count = deactives_futures_signals.filter(
            status='فول تارگت').count() + deactives_spot_signals.filter(status='فول تارگت').count()
            
        closed_at_loss_count = deactives_futures_signals.filter(status='حد ضرر فعال شد').count(
        ) + deactives_spot_signals.filter(status='حد ضرر فعال شد').count()
        
        voided_count = deactives_futures_signals.filter(status='باطل شد').count(
        ) + deactives_spot_signals.filter(status='باطل شد').count()
        
        risk_free_count = deactives_futures_signals.filter(status__icontains='ریسک فری').count(
        ) + deactives_spot_signals.filter(status__icontains='ریسک فری').count()
        
        spot_sum = SpotSignal.objects.filter(is_active=False).aggregate(
            Sum('profit_of_signal_amount')).get('profit_of_signal_amount__sum')
        if spot_sum is None:
            spot_sum = 0

        futures_sum = FuturesSignal.objects.filter(is_active=False).aggregate(
            Sum('profit_of_signal_amount')).get('profit_of_signal_amount__sum')
        if futures_sum is None:
            futures_sum = 0

        deactive_signal_count = deactives_futures_signals.count() + \
            deactives_spot_signals.count()
        if deactive_signal_count == 0:
            deactive_signal_count = 1
        profit_value = ceil((futures_sum + spot_sum))

        res = {
            'closed_with_profit_count': closed_with_profit_count,
            'closed_at_loss_count': closed_at_loss_count,
            'voided_count': voided_count,
            'risk_free_count': risk_free_count,
            'profit_value': profit_value,
            'signals': FuturesSignalSerializer(deactives_futures_signals, many=True).data + SpotSignalSerializer(deactives_spot_signals, many=True).data
        }

        return Response(res)


class DeactiveSpotSignal(APIView):
    def get(self, request):
        signal = SpotSignal.objects.get(id=request.query_params.get('id'))
        last_touched_target = get_prev_touched_target(signal)
        if signal.is_active:
            content = ''
            status = request.query_params.get('status')
            if 'حد ضرر' in status:
                if signal.is_touched_entry:
                    signal.is_active = False
                    signal.status = status
                    signal.profit_of_signal_amount = 0
                    content = 'حد ضرر فعال شد'
                    send_notification(f'سیگنال {signal.coin_symbol}', content)
                    send_notification(
                        f'سیگنال {signal.coin_symbol}', 'بسته شد')

            else:
                if signal.targets.last().is_touched:
                    signal.is_active = False
                    signal.status = status
                    signal.profit_of_signal_amount = (
                        (signal.entry - last_touched_target.amount) / signal.entry) * 100
                    content = 'فول تارگت'
                    send_notification(f'سیگنال {signal.coin_symbol}', content)
                    send_notification(
                        f'سیگنال {signal.coin_symbol}', 'بسته شد')
            signal.save()
        return Response({'message': 'ok'}, 200)


class DeactiveFuturesSignal(ListAPIView):
    def get(self, request):
        signal = FuturesSignal.objects.get(id=request.query_params.get('id'))
        last_touched_target = get_prev_touched_target(signal)
        if signal.is_active:
            status = request.query_params.get('status')
            if 'حد ضرر' in status:
                if signal.is_touched_entry:
                    signal.is_active = False
                    signal.status = status
                    signal.profit_of_signal_amount = 0
                    send_notification(
                        f'سیگنال {signal.coin_symbol}', status)

            else:
                signal.is_active = False
                signal.status = status
                signal.profit_of_signal_amount = abs((
                    ((signal.entry - last_touched_target.amount) / signal.entry) * 100) * signal.leverage)
                send_notification(
                    f'سیگنال {signal.coin_symbol}', status)
            send_notification(f'سیگنال {signal.coin_symbol}', 'بسته شد')
            signal.save()
        return Response({'message': 'ok'}, 200)


class SetTouchTarget(ListAPIView):
    def get(self, request):
        kind = request.query_params.get('kind')
        selected_target = Target.objects.get(id=request.query_params.get('id'))
        global title
        global content
        content = f'{selected_target.title} تاچ شد'
        
        if kind == 'spot':
            signal = SpotSignal.objects.get(
                id=request.query_params.get('signal_id'))
            title = f'سیگنال {signal.coin_symbol}'
        elif kind == 'futures':
            signal = FuturesSignal.objects.get(
                id=request.query_params.get('signal_id'))
            title = f'سیگنال {signal.coin_symbol}'
            

        if is_first_target_touched(signal, selected_target):
            signal.alarms.add(SignalAlarm.objects.create(title='ریسک فری! حدضرر را نقطه ورود تنطیم کنید'))
            signal.stop_loss = signal.entry
            signal.save()
            content += ' - رعایت ریسک فری'
        else:
            prev_touched_target = get_prev_touched_target(signal)
            alarm = signal.alarms.filter(title__icontains='ریسک فری').first()
            alarm.title = f'ریسک فری! حدضرر را {prev_touched_target.title} تنطیم کنید'
            alarm.save()
            signal.stop_loss = prev_touched_target.amount
            signal.save()

        if not selected_target.is_touched:
            selected_target.is_touched = True
            selected_target.save()
            send_notification(title, content)
        return Response({'message': 'ok'}, 200)


class SetTouchSpotEntry(ListAPIView):
    def get(self, request):
        signal = SpotSignal.objects.get(id=request.query_params.get('id'))
        if not signal.is_touched_entry:
            signal.is_touched_entry = True
            signal.save()
            send_notification(f'سیگنال {signal.coin_symbol}', 'فعال شد')
        return Response({'message': 'ok'}, 200)


class SetTouchFuturesEntry(ListAPIView):
    def get(self, request):
        signal = FuturesSignal.objects.get(id=request.query_params.get('id'))
        if not signal.is_touched_entry:
            signal.is_touched_entry = True
            signal.save()
            send_notification(f'سیگنال {signal.coin_symbol}', 'فعال شد')
        return Response({'message': 'ok'}, 200)


class getSignalGeneralStats(APIView):
    def get(self, request):
        active_signal_count = SpotSignal.objects.filter(
            is_active=True).count() + FuturesSignal.objects.filter(is_active=True).count()
        deactive_signal_count = SpotSignal.objects.filter(is_active=False).count(
        ) + FuturesSignal.objects.filter(is_active=False).count()
        profit_of_signal_amount = calculate_profit_of_signals('monthly')
        profit_of_signal_amount_weekly = calculate_profit_of_signals('weekly')
        profit_of_signal_amount_daily = calculate_profit_of_signals('daily')
        response = {
            'profit_of_signal_amount': profit_of_signal_amount,
            'profit_of_signal_amount_weekly': profit_of_signal_amount_weekly,
            'profit_of_signal_amount_daily': profit_of_signal_amount_daily,
            'active_signal_count': active_signal_count,
            'deactive_signal_count': deactive_signal_count,
        }
        return Response(response)


class GetThreeLastBanners(APIView):
    authentication_classes = []  # disabled authentication
    permission_classes = []  # disabled permission

    def get(self, request):
        three_last_banners = Banner.objects.all().order_by('-id')[:3]
        banner_serializer = BannerSerializer(three_last_banners, many=True)
        return Response(banner_serializer.data, status_code.HTTP_200_OK)


class GetGiftsInfo(APIView):
    def get(self, request):
        gifts = UserGift.objects.filter(user=request.user.id)
        all_blue_b_card = gifts.filter(gift_type="blue-b")
        blue_b_card_actives = all_blue_b_card.filter(is_active=True)
        blue_b_card_deactives = all_blue_b_card.filter(is_active=False)

        all_black_b_card = gifts.filter(gift_type="black-b")
        black_b_card_actives = all_black_b_card.filter(is_active=True)
        black_b_card_deactives = all_black_b_card.filter(is_active=False)

        all_red_b_card = gifts.filter(gift_type="red-b")
        red_b_card_actives = all_red_b_card.filter(is_active=True)
        red_b_card_deactives = all_red_b_card.filter(is_active=False)

        result = {
            'blue_b': {
                'code': str(all_blue_b_card.last().code) if all_blue_b_card.last() != None else None,
                'all_card_count': all_blue_b_card.count(),
                'active_count': blue_b_card_actives.count(),
                'deactive_count': blue_b_card_deactives.count(),
            },
            'red_b': {
                'code': str(all_red_b_card.last().code) if all_red_b_card.last() != None else None,
                'all_card_count': all_red_b_card.count(),
                'active_count': red_b_card_actives.count(),
                'deactive_count': red_b_card_deactives.count(),
            },
            'black_b': {
                'code': str(all_black_b_card.last().code) if all_black_b_card.last() != None else None,
                'all_card_count': all_black_b_card.count(),
                'active_count': black_b_card_actives.count(),
                'deactive_count': black_b_card_deactives.count(),
            },
            'invated_count': request.user.invated_users.count(),
            'buy_with_user_code': gifts.filter(for_what="buy", gift_type="black-b").count(),
            'wallet_amount': request.user.wallet,
            'user_code': request.user.id
        }

        return Response(result, status=status_code.HTTP_200_OK)


class UseGiftAPI(APIView):
    def post(self, request):
        gift_type = request.data.get('gift_type', None)
        gift_item = request.data.get('gift_item', None)
        code = None
        gift_detail = ''
        selected_user_gift = UserGift.objects.filter(
            gift_type=gift_type, user=request.user, is_active=True).first()
        if selected_user_gift is not None:
            if selected_user_gift.gift_type == 'red-b':
                if gift_item == 'free-transaction':
                    user_transaction = Transaction.objects.filter(
                        user=self.request.user).first()
                    if user_transaction is not None:
                        user_transaction.validity_rate += 15
                        user_transaction.save()
                    else:
                        Transaction.objects.create(payment_mode="offline", amount=0, transaction_status="تایید شده", validity_rate=15, user=request.user,
                                                   is_send_receipt=True, is_confirmation=True, date_of_approval=now(), special_item=SpecialAccountItem.objects.first())
                    UserGiftLog.objects.create(
                        title='اشتراک رایگان', content="15 روزه", user=request.user)
                    gift_detail = '15 روز اشتراک رایگان'
                elif gift_item == 'discount':
                    code = get_random_string(10)
                    DiscountCode.objects.create(
                        code=code, percentage=50, count=1, is_private=True, validity_date=now() + timedelta(int(100)))
                    UserGiftLog.objects.create(
                        title='کد تخفیف 50 درصد', content=code, user=request.user)
                    gift_detail = code

            if selected_user_gift.gift_type == 'blue-b':
                if gift_item == 'free-transaction':
                    user_transaction = Transaction.objects.filter(
                        user=self.request.user).first()
                    if user_transaction is not None:
                        user_transaction.validity_rate += 10
                        user_transaction.save()
                    else:
                        Transaction.objects.create(payment_mode="offline", amount=0, transaction_status="تایید شده", validity_rate=10, user=request.user,
                                                   is_send_receipt=True, is_confirmation=True, date_of_approval=now(), special_item=SpecialAccountItem.objects.first())
                    UserGiftLog.objects.create(
                        title='اشتراک رایگان', content="10 روزه", user=request.user)
                    gift_detail = '10 روز اشتراک رایگان'
                elif gift_item == 'discount':
                    code = get_random_string(10)
                    DiscountCode.objects.create(
                        code=code, percentage=30, count=1, is_private=True, validity_date=now() + timedelta(int(100)))
                    UserGiftLog.objects.create(
                        title='کد تخفیف 30 درصد', content=code, user=request.user)
                    gift_detail = code

            elif selected_user_gift.gift_type == 'black-b':
                if gift_item == 'free-transaction':
                    user_transaction = Transaction.objects.filter(
                        user=self.request.user).first()
                    if user_transaction is not None:
                        user_transaction.validity_rate += 30
                        user_transaction.save()
                    else:
                        Transaction.objects.create(payment_mode="offline", amount=0, transaction_status="تایید شده", validity_rate=30, user=request.user,
                                                   is_send_receipt=True, is_confirmation=True, date_of_approval=now(), special_item=SpecialAccountItem.objects.first())
                    UserGiftLog.objects.create(
                        title='اشتراک رایگان', content="1 ماه", user=request.user)
                    gift_detail = '1 ماه اشتراک رایگان'
                elif gift_item == 'cash':
                    trx = selected_user_gift.transaction
                    user_share_amount = (10 * trx.amount) / 100
                    request.user.wallet += user_share_amount
                    request.user.save()
                    gift_detail = f'{user_share_amount} تومان'
                    UserGiftLog.objects.create(
                        title='افزایش اعتبار', content=f'{user_share_amount} تومان', user=request.user)
                    last_black_b_card = UserGift.objects.filter(
                        gift_type='black-b', user=request.user, is_active=True).last()
                    send_sms('gtc2lktr0mvn6o6', request.user.phone_number, {'cart': str(last_black_b_card.code), 'price': str(
                        user_share_amount), 'date': get_now_jalali_date(), 'mojodi': str(request.user.wallet)})

            selected_user_gift.is_active = False
            selected_user_gift.save()

            return Response({'message': 'ok', 'info': {'gift_type': 'red-b', 'gift_item': gift_item, 'discount': code, 'gift_detail': gift_detail}})
        return Response({'message': 'card not found'}, status=status_code.HTTP_404_NOT_FOUND)


class GetUserGiftLogsAPI(APIView):
    def get(self, request):
        logs = UserGiftLog.objects.filter(user=request.user).order_by('-id')
        serializer = UserGiftLogSerializer(logs, many=True)
        return Response(serializer.data, status=status_code.HTTP_200_OK)


class CreateUserCashWithdrawalAPI(CreateAPIView):
    queryset = UserCashWithdrawal.objects.all()
    serializer_class = UserCashWithdrawalSerializer

    def create(self, request, *args, **kwargs):
        amount = self.request.data.get('amount', None)
        user = request.user
        user.wallet -= int(amount)
        user.save()
        return super().create(request, *args, **kwargs)


class SeenAllSignalNews(APIView):
    def get(self, request):
        signal_id = request.query_params.get('signal_id', None)
        kind = request.query_params.get('kind', None)
        if kind == 'futures':
            signal = FuturesSignal.objects.filter(id=signal_id).first()
            if signal is not None:
                for news in signal.signal_news.all():
                    news.seen_by.add(request.user)
                    news.save()
        else:
            signal = SpotSignal.objects.filter(id=signal_id).first()
            if signal is not None:
                for news in signal.signal_news.all():
                    news.seen_by.add(request.user)
                    news.save()

        return Response({'message': 'ok'})

    
class CheckUserTransactionStatus(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(
            is_send_receipt=True, is_confirmation=False)
        for transaction in transactions:
            # minutes
            result = diff_between_two_dates(
                now(), transaction.last_updated_time).seconds / 60
            if result >= 3 and transaction.transaction_status != 'در صف ورود' and transaction.transaction_status != 'ارسال به مرکز کنترل' and transaction.transaction_status != 'در حال بررسی':
                transaction.transaction_status = 'در صف ورود'
                transaction.last_updated_time = now()
                transaction.save()
            elif result >= 5 and transaction.transaction_status == 'در صف ورود':
                transaction.transaction_status = 'ارسال به مرکز کنترل'
                transaction.last_updated_time = now()
                transaction.save()
            elif result >= 30 and transaction.transaction_status == 'ارسال به مرکز کنترل':
                transaction.transaction_status = 'در حال بررسی'
                transaction.last_updated_time = now()
                transaction.save()
        return Response({'message': 'ok'})


class CheckUserSpecialAccount(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(is_confirmation=True)
        for transaction in transactions:
            result = diff_between_two_dates(
                transaction.date_of_approval + timedelta(transaction.validity_rate + 1), now()).days
            if result == 10:
                send_sms('np5tviaoag', str(transaction.user.phone_number), {
                         'date_cnt': str(result)})
            elif result == 5:
                send_sms('np5tviaoag', str(transaction.user.phone_number), {
                         'date_cnt': str(result)})
            elif result == 3:
                send_sms('np5tviaoag', str(transaction.user.phone_number), {
                         'date_cnt': str(result)})
            elif result == 1:
                send_sms('np5tviaoag', str(transaction.user.phone_number), {
                         'date_cnt': str(result)})
            elif result <= 0:
                send_sms('3egblee8ys', str(transaction.user.phone_number), {
                         'name': transaction.user.full_name.split()[0]})
                transaction.delete()
        return Response({'message': 'ok'})


class OrderBaskets(ListAPIView):
    queryset = Basket.objects.filter(is_accept_participant=True)
    serializer_class = BasketSerializer



class CheckUserAPIsKucoin(APIView):
    def post(self, request):
        futuresAPIKey = request.data.get('futuresAPIKey', 'None')
        futuresSecret = request.data.get('futuresSecret', 'None')
        futuresPassphrase = request.data.get('futuresPassphrase', 'None')
        spotAPIKey = request.data.get('spotAPIKey', 'None')
        spotSecret = request.data.get('spotSecret', 'None')
        spotPassphrase = request.data.get('spotPassphrase', 'None')

        if (futuresAPIKey == 'None' or spotAPIKey == 'None') and request.user.user_kucoin_api is not None:
            user_apis = request.user.user_kucoin_api
            futuresAPIKey = user_apis.futures_api_key
            futuresSecret = user_apis.futures_secret
            futuresPassphrase = user_apis.futures_passphrase
            spotAPIKey = user_apis.spot_api_key
            spotSecret = user_apis.spot_secret
            spotPassphrase = user_apis.spot_passphrase

        api_key = spotAPIKey
        api_secret = spotSecret
        api_passphrase = spotPassphrase
        url = 'https://api.kucoin.com/api/v1/accounts'
        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
        signature = base64.b64encode(
            hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        spot_response = requests.request('get', url, headers=headers)

        api_key = futuresAPIKey
        api_secret = futuresSecret
        api_passphrase = futuresPassphrase
        url = 'https://api-futures.kucoin.com/api/v1/position?symbol=USDTUSDM'
        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + '/api/v1/position?symbol=USDTUSDM'
        signature = base64.b64encode(
            hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        futures_response = requests.request('get', url, headers=headers)

        if futures_response.status_code == 200 and spot_response.status_code == 200:
            user_kocoin_api = UserKucoinAPI.objects.create(futures_api_key=futuresAPIKey, futures_secret=futuresSecret, futures_passphrase=futuresPassphrase,
             spot_api_key=spotAPIKey, spot_secret=spotSecret, spot_passphrase=spotPassphrase)
            if request.user.user_kucoin_api is not None:
                request.user.user_kucoin_api.delete()
            request.user.user_kucoin_api = user_kocoin_api
            request.user.save()
        return Response({'spot': spot_response.status_code, 'futures': futures_response.status_code})


class joinToBasket(APIView):
    def get(self, request, basket_id):
        user_active_basket_joined = Basket.objects.filter(participants__in=[request.user.id], is_active=True).count()
        print(user_active_basket_joined)
        if user_active_basket_joined == 0:
            selected_basket = Basket.objects.filter(id=basket_id).first()
            user_usdt_balance = check_user_usdt_balance(request.user)
            if float(user_usdt_balance.get('balance')) >= float(selected_basket.initial_balance):
                selected_basket.participants.add(request.user)
                selected_basket.save()
                return Response({'status': 'ok', 'message': 'شما عضو سبد شدید'}, status=status_code.HTTP_200_OK)
            return Response({'status': 'error', 'message': 'موجودی شما کافی نیست'}, status=status_code.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': 'شما هم اکنون سبد فعال دارید'}, status=status_code.HTTP_400_BAD_REQUEST)
        
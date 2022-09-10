from dataclasses import fields
from urllib import request
import uuid
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import Device, User, UserCashWithdrawal, UserGift, UserGiftLog, UserMessage, VerificationCode
from banner.models import Banner
from copy_trade.models import Basket, Stage
from news.models import Category, News
from django.utils.timezone import now
from signals.models import FuturesSignal, SignalAlarm, SignalNews, SpotSignal, Target
from story.models import Story
from transaction.models import Transaction, DiscountCode
from special_account_item.models import SpecialAccountItem
from utilities import diff_between_two_dates, generate_token


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()
    pk = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['full_name', 'phone_number',
                  'national_code', 'password', 'device', 'is_foreigner', 'pk']

    def create(self, validated_data):
        if validated_data.get('is_foreigner', False) == True:
            validated_data['is_phone_number_verified'] = True
        username = uuid.uuid4()
        device = Device.objects.create(**validated_data['device'])
        del validated_data['device']
        identifier_code = validated_data['pk']
        del validated_data['pk']
        user = User.objects.create_user(
            **validated_data, device=device, username=username)
        invater = User.objects.filter(id=identifier_code).first()
        if invater is not None:
            invater.invated_users.add(user)
            if invater.invated_users.all().count() % 7 == 0:
                UserGift.objects.create(
                    user=invater, gift_type='blue-b', for_what="register")
        self.context['request'].user = user
        return user


class UserLoginWithPasswordSerializer(serializers.ModelSerializer):
    phone_number = serializers.IntegerField()
    device_uuid = serializers.CharField()

    class Meta:
        model = User
        fields = ['password', 'phone_number', 'device_uuid']

    def validate(self, data):
        password = data.get('password', None)
        phone_number = data.get('phone_number', None)
        device_uuid = data.get('device_uuid', None)
        user = User.objects.filter(phone_number=phone_number).first()
        if user.device is not None and user.device.uuid is None:
            generate_token(user)
            user.device.uuid = device_uuid
            user.device.save()
        else:
            if user.device.uuid != device_uuid:
                raise serializers.ValidationError(
                    'This UUID does not match the user UUID.')
        user = authenticate(
            self.context['request'], username=user.username, password=password)
        if user is not None:
            self.context['request'].user = user
            return super().validate(data)
        raise serializers.ValidationError('Password is incorrect.')

    def validate_phone_number(self, phone_number):
        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise serializers.ValidationError(
                'This phone number dose not exists.')
        elif not user.is_phone_number_verified:
            raise serializers.ValidationError(
                'This phone number has not yet been verified.')
        return phone_number


class UserLoginVerificationCodeSerializer(serializers.ModelSerializer):
    phone_number = serializers.IntegerField()
    verification_code = serializers.IntegerField()
    device_uuid = serializers.CharField()

    class Meta:
        model = User
        fields = ['phone_number', 'device_uuid', 'verification_code']

    def validate(self, data):
        phone_number = data.get('phone_number', None)
        device_uuid = data.get('device_uuid', None)
        verification_code = data.get('verification_code', None)
        user = User.objects.filter(phone_number=phone_number).first()
        if user.device is not None and user.device.uuid is None:
            generate_token(user)
            user.device.uuid = device_uuid
            user.device.save()
        else:
            if user.device.uuid != device_uuid:
                raise serializers.ValidationError(
                    'This UUID does not match the user UUID.')
        verification = VerificationCode.objects.filter(
            user=user, code=verification_code).last()

        if verification is not None:
            if not verification.is_expire:
                self.context['request'].user = user
                return data
            raise serializers.ValidationError('This code is expired.')
        raise serializers.ValidationError('This code is invalid.')

    def validate_phone_number(self, phone_number):
        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise serializers.ValidationError(
                'This phone number dose not exists.')
        return phone_number


class NewsSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    updated_time = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = '__all__'

    def get_updated_time(self, obj):
        current = now()
        updated_time = obj.updated_time
        diff_dates = diff_between_two_dates(current, updated_time)
        if 0 < diff_dates.days < 30:
            return f'{diff_dates.days} روز پیش'
        elif 30 <= diff_dates.days < 365:
            return f'{int(diff_dates.days / 30)} ماه پیش'
        elif diff_dates.days >= 365:
            return f'{int(diff_dates.days / 365)} سال پیش'

        diff_dates_minute = int(diff_dates.seconds / 60)
        if 0 <= diff_dates_minute <= 5:
            return 'لحظاتی پیش'
        elif 5 < diff_dates_minute < 60:
            return f'{diff_dates_minute} دقیقه پیش'
        elif diff_dates_minute >= 60:
            return f'{int(diff_dates_minute/60)} ساعت پیش'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SpecialAccountItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialAccountItem
        fields = ['id', 'title', 'price', 'expire_day']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_active', 'full_name', 'phone_number', 'national_code', 'from_city', 'amount_of_capital',
                  'familiarity_with_digital_currencies', 'get_to_know_us', 'id_card', 'face', 'is_full_authentication',
                  'is_receive_signal_notifications', 'is_receive_news_notifications', 'father_name', 'date_of_birth', 'place_of_issue']


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['code', 'percentage']


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = '__all__'


class CheckDiscountCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):
        this_code = DiscountCode.objects.filter(
            code=code, is_active=True, validity_date__gt=datetime.now()).first()
        if this_code is None:
            raise serializers.ValidationError('This code dose not exists.')
        if this_code.count <= 0:
            raise serializers.ValidationError('This code number has expired.')
        if self.context['request'].user in this_code.use_by.all():
            raise serializers.ValidationError('You already use this code.')
        this_code.count -= 1
        this_code.save()
        self.context['request'].discount_code = this_code
        return code


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['amount'] == 0:
            transaction = Transaction.objects.create(**validated_data)
            transaction.is_confirmation = True
            transaction.date_of_approval = now()
            transaction.is_send_receipt = True
            transaction.transaction_status = "تایید شده"
            transaction.save()
        else:
            transaction = Transaction.objects.create(**validated_data)

        return transaction


class SignalNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalNews
        fields = '__all__'


class SignalAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalAlarm
        fields = ['id', 'title']


class SignalTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'


class FuturesSignalSerializer(serializers.ModelSerializer):
    targets = SignalTargetSerializer(many=True, read_only=True)
    signal_news = SignalNewsSerializer(many=True, read_only=True)
    alarms = SignalAlarmSerializer(many=True, read_only=True)

    class Meta:
        model = FuturesSignal
        fields = '__all__'


class SpotSignalSerializer(serializers.ModelSerializer):
    targets = SignalTargetSerializer(many=True, read_only=True)
    signal_news = SignalNewsSerializer(many=True, read_only=True)
    alarms = SignalAlarmSerializer(many=True, read_only=True)

    class Meta:
        model = SpotSignal
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class UserGiftLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGiftLog
        fields = '__all__'


class UserCashWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCashWithdrawal
        fields = '__all__'

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True)
    trader = serializers.StringRelatedField()
    class Meta:
        model = Basket
        fields = '__all__'

class UserStorySerializer(serializers.ModelSerializer):
    is_all_story_visited = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'is_all_story_visited', 'user_image']

    def get_is_all_story_visited(self, obj):
        user = obj
        last_user_story  = Story.objects.filter(user=user, expire_time__gt=now()).last()
        return last_user_story.visitors.filter(id=self.context['request'].user.id).first() is not None

class StorySerializer(serializers.ModelSerializer):
    is_visited = serializers.SerializerMethodField()
    user = UserStorySerializer()

    class Meta:
        model = Story
        exclude = ['visitors']

    def get_is_visited(self, obj):
        user = self.context['request'].user
        return obj.visitors.filter(id=user.id).first() is not None
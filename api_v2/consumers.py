import json
import jdatetime
from news.models import News
from .serializer import NewsSerializer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'news'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_news',
            }
        )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_news',
            }
        )


    async def send_news(self, event):
        self.news = await self.get_news()
        await self.send(json.dumps(self.news))

    
    @database_sync_to_async
    def get_news(self):
        news = News.objects.all().order_by('-id')
        news_serializer = NewsSerializer(news, many=True).data
        for i, data in enumerate(news_serializer):
            original_date = news[i].updated_time
            jalali_datetime = jdatetime.GregorianToJalali(original_date.year, original_date.month, original_date.day).getJalaliList()
            news_serializer[i]['updated_time'] = self.normalized_date(jalali_datetime, original_date)
        result = {'data': news_serializer}
        return result

    

    def get_month_number(self, month_number):
        if (month_number == 1):
            return 'فروردین'
        elif (month_number == 2):
            return 'اردیبهشت'
        elif (month_number == 3):
            return 'خرداد'
        elif (month_number == 4):
            return 'تیر'
        elif (month_number == 5):
            return 'مرداد'
        elif (month_number == 6):
            return 'شهریور'
        elif (month_number == 7):
            return 'مهر'
        elif (month_number == 8):
            return 'آبان'
        elif (month_number == 9):
            return 'آذر'
        elif (month_number == 10):
            return 'دی'
        elif (month_number == 11):
            return 'بهمن'
        elif (month_number == 12):
            return 'اسفند'

    def normalized_date(self, jdate, gdate):
        new_date = list(jdate)
        new_date[1] = self.get_month_number(new_date[1])
        week_name = gdate.strftime('%A')
        week_name = week_name.replace('Saturday', 'شنبه')
        week_name = week_name.replace('Sunday', 'یک شنبه')
        week_name = week_name.replace('Monday', 'دوشنبه')
        week_name = week_name.replace('Tuesday', 'سه شنبه')
        week_name = week_name.replace('Wednesday', 'چهار شنبه')
        week_name = week_name.replace('Thursday', 'پنج شنبه')
        week_name = week_name.replace('Friday', 'جمعه')
        result = f'{week_name} {new_date[2]} {new_date[1]} {new_date[0]}' 
        return result

class GetThreeLastNewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'news'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_news',
            }
        )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_news',
            }
        )


    async def send_news(self, event):
        self.news = await self.get_news()
        await self.send(json.dumps(self.news))

    @database_sync_to_async
    def get_news(self):
        news = News.objects.all().order_by('-id')[:3]
        news_serializer = NewsSerializer(news, many=True).data
        for i, data in enumerate(news_serializer):
            original_date = news[i].updated_time
            jalali_datetime = jdatetime.GregorianToJalali(original_date.year, original_date.month, original_date.day).getJalaliList()
            news_serializer[i]['updated_time'] = self.normalized_date(jalali_datetime, original_date)
        result = {'data': news_serializer}
        return result

    def normalized_date(self, jdate, gdate):
        new_date = list(jdate)
        new_date[1] = self.get_month_number(new_date[1])
        week_name = gdate.strftime('%A')
        week_name = week_name.replace('Saturday', 'شنبه')
        week_name = week_name.replace('Sunday', 'یک شنبه')
        week_name = week_name.replace('Monday', 'دوشنبه')
        week_name = week_name.replace('Tuesday', 'سه شنبه')
        week_name = week_name.replace('Wednesday', 'چهار شنبه')
        week_name = week_name.replace('Thursday', 'پنج شنبه')
        week_name = week_name.replace('Friday', 'جمعه')
        result = f'{week_name} {new_date[2]} {new_date[1]} {new_date[0]}' 
        return result

    def get_month_number(self, month_number):
        if (month_number == 1):
            return 'فروردین'
        elif (month_number == 2):
            return 'اردیبهشت'
        elif (month_number == 3):
            return 'خرداد'
        elif (month_number == 4):
            return 'تیر'
        elif (month_number == 5):
            return 'مرداد'
        elif (month_number == 6):
            return 'شهریور'
        elif (month_number == 7):
            return 'مهر'
        elif (month_number == 8):
            return 'آبان'
        elif (month_number == 9):
            return 'آذر'
        elif (month_number == 10):
            return 'دی'
        elif (month_number == 11):
            return 'بهمن'
        elif (month_number == 12):
            return 'اسفند'
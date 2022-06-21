from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('news/', consumers.NewsConsumer.as_asgi()),
    path('three-last-news/', consumers.GetThreeLastNewsConsumer.as_asgi()),
]
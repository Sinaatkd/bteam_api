from django.contrib import admin
from .models import SignalNews, FuturesSignal, SpotSignal, Target

admin.site.register(SignalNews)
admin.site.register(FuturesSignal)
admin.site.register(SpotSignal)
admin.site.register(Target)
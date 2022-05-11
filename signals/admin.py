from django.contrib import admin
from .models import SignalAlarm, SignalNews, FuturesSignal, SpotSignal, Target

admin.site.register(SignalNews)
admin.site.register(FuturesSignal)
admin.site.register(SpotSignal)
admin.site.register(Target)
admin.site.register(SignalAlarm)

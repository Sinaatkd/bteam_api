from django.contrib import admin
from django.contrib.auth.models import Permission
from account.models import Device, User, UserCashWithdrawal, UserGift, UserGiftLog, UserMessage, VerificationCode

# Register your models here.
admin.site.register(Device)
admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(UserMessage)
admin.site.register(Permission)
admin.site.register(UserGift)
admin.site.register(UserGiftLog)
admin.site.register(UserCashWithdrawal)

from django.urls import path

from api_v2.views import CancelTransactionAPI, CreateTransactionAPI, CheckDiscountCodeAPI, CreateUserCashWithdrawalAPI, DeactiveFuturesSignal, DeactiveSpotSignal, \
    EditUserAPI, ForgotPassAPI, GetAllActiveFuturesSignals, GetAllActiveFuturesSignals, GetAllDeactiveSignals, GetAllPublicDiscountAPI, GetAllActiveSpotSignals, GetGiftsInfo, \
    GetSpecialAccountItemListAPI, GetUserGiftLogsAPI, GetUserInfoAPI, GetUserMessages, \
    LoginUserWithUserPassAPI, LoginUserWithVerificationCodeAPI, RegisterUserAPI, SeenAllSignalNews, SeenAllUserMessage, SendReceiptImageAPI, \
    SendVerificationCodeAPI, SetTouchFuturesEntry, SetTouchSpotEntry, SetTouchTarget, UseGiftAPI, getSignalGeneralStats, GetThreeLastBanners

urlpatterns = [
    path('user/', GetUserInfoAPI.as_view()),
    path('user/messages/', GetUserMessages.as_view()),
    path('user/messages/seen-all/', SeenAllUserMessage.as_view()),
    path('user/<int:pk>/', EditUserAPI.as_view()),
    path('forgot-pass/', ForgotPassAPI.as_view()),
    path('register/', RegisterUserAPI.as_view()),
    path('login/phone-pass/', LoginUserWithUserPassAPI.as_view()),
    path('login/verification-code/', LoginUserWithVerificationCodeAPI.as_view()),
    path('send-verification-code/', SendVerificationCodeAPI.as_view()),
    path('special-account-items/', GetSpecialAccountItemListAPI.as_view()),
    path('creaet-transaction/', CreateTransactionAPI.as_view()),
    path('cancel-transaction/', CancelTransactionAPI.as_view()),
    path('discount-codes/', GetAllPublicDiscountAPI.as_view()),
    path('check-discount-code/', CheckDiscountCodeAPI.as_view()),
    path('send-receipt/<int:pk>/', SendReceiptImageAPI.as_view()),
    path('signals/futures/', GetAllActiveFuturesSignals.as_view()),
    path('signals/news/', SeenAllSignalNews.as_view()),
    path('signals/futures/deactive/', DeactiveFuturesSignal.as_view()),
    path('signals/spot/', GetAllActiveSpotSignals.as_view()),
    path('signals/spot/deactive/', DeactiveSpotSignal.as_view()),
    path('signals/general-stats/', getSignalGeneralStats.as_view()),
    path('signals/touch-target/', SetTouchTarget.as_view()),
    path('signals/spot/touch-entry/', SetTouchSpotEntry.as_view()),
    path('signals/futures/touch-entry/', SetTouchFuturesEntry.as_view()),
    path('signals/efficiency/', GetAllDeactiveSignals.as_view()),
    path('banners/', GetThreeLastBanners.as_view()),
    path('gifts-info/', GetGiftsInfo.as_view()),
    path('use-gift/', UseGiftAPI.as_view()),
    path('gifs-log/', GetUserGiftLogsAPI.as_view()),
    path('create-cash-withdrawal/', CreateUserCashWithdrawalAPI.as_view()),
]

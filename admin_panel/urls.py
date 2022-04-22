from unicodedata import name
from django.urls import path

from django.contrib.auth.decorators import login_required
from admin_panel.views.auth_view import admin_login
from admin_panel.views.cash_withdrawal_view import CashWithdrawalList, confirm_cash_withdrawal, delete_cash_withdrawal
from admin_panel.views.news_view import NewsList, add_new, delete_news
from admin_panel.views.special_account_view import SpecialAccountItemList, add_special_account, delete_special_account
from .views.spot_signal_view import SpotSignalsList, delete_spot_signal, detail_spot ,close_spot_signal ,add_spot_target ,add_spot_news ,add_spot_signal
from .views.gift_view import UsersList as UserListGifts, deactive_user_gift, user_gifts_detail, active_user_gift, add_gift
from .views.futures_signal_view import FuturesSignalsList, add_futures_news, add_futures_signal, add_futures_target, close_futures_signal, delete_futures_signal, detail_futures
from .views.transaction_view import DiscountCodesList, TransactionsList, add_discount_code, active_discount_code, confirm_transaction, deactive_discount_code, set_private_discount, set_public_discount, unconfirm_transaction
from .views.user_views import UsersList, delete_user, add_user_message, home_page, remove_device_uuid, user_edit, deactivate_user, activate_user, set_user_permission

urlpatterns = [
    path('', login_required(home_page), name='home'),
    path('users/', login_required(UsersList.as_view()), name='users_list'),
    path('transactions/', login_required(TransactionsList.as_view()), name='transactions_list'),
    path("discount-codes/", DiscountCodesList.as_view(), name="discount_codes_list"),
    path("set-public-discount/<discount_code_id>/", set_public_discount, name="set_public_discount"),
    path("set-private-discount/<discount_code_id>/", set_private_discount, name="set_private_discount"),
    path("active-discount-code/<discount_code_id>/", deactive_discount_code, name="deactive_discount_code"),
    path("deactive-discount-code/<discount_code_id>/", active_discount_code, name="active_discount_code"),
    path("add-discount-code/", add_discount_code, name="add_discount_code"),
    path('add-user-message/', login_required(add_user_message), name='add_user_message'),
    path('user/<int:pk>/edit/', login_required(user_edit), name='user_edit'),
    path('users/detail/<int:user_id>/deactivate/', login_required(deactivate_user), name='deactivate_user'),
    path('users/detail/<int:user_id>/delete/', login_required(delete_user), name='delete_user'),
    path('users/detail/<int:user_id>/activate/', login_required(activate_user), name='activate_user'),
    path('users/set-permission/<int:user_id>/', login_required(set_user_permission), name='set_user_permission'),
    path('transactions/confirm/<transaction_id>/', login_required(confirm_transaction), name='confirm_transaction'),
    path('transactions/unconfirm/<transaction_id>/', login_required(unconfirm_transaction), name='unconfirm_transaction'),
    path('device/remove-uuid/<device_id>/', login_required(remove_device_uuid), name='remove_device_uuid'),
    path('news/', login_required(NewsList.as_view()), name='news_list'),
    path('news/add-new/', login_required(add_new), name='add_new'),
    path('news/delete/<news_id>/', login_required(delete_news), name='delete_news'),
    path('special-account-item/', login_required(SpecialAccountItemList.as_view()), name='special_account_item_list'),
    path('special-account-item/add-new/', login_required(add_special_account), name='special_account_new'),
    path('special-account-item/delete/<special_account_id>/', login_required(delete_special_account), name='delete_special_account'),
    path('signals/futures/', login_required(FuturesSignalsList.as_view()), name='signal_futures_list'),
    path('signals/futures/detail/<futures_id>/', login_required(detail_futures), name='detail_futures'),
    path('signals/futures/delete/<futures_id>/', login_required(delete_futures_signal), name='delete_futures_signal'),
    path('signals/futures/close/<futures_id>/', login_required(close_futures_signal), name='close_futures_signal'),
    path('signals/futures/add-target/', login_required(add_futures_target), name='add_futures_target'),
    path('signals/futures/add-news/', login_required(add_futures_news), name='add_futures_news'),
    path('signals/futures/add/', login_required(add_futures_signal), name='add_futures_signal'),
    path('signals/spot/', login_required(SpotSignalsList.as_view()), name='signal_spot_list'),
    path('signals/spot/detail/<spot_id>/', login_required(detail_spot), name='detail_spot'),
    path('signals/spot/delete/<spot_id>/', login_required(delete_spot_signal), name='delete_spot_signal'),
    path('signals/spot/close/<spot_id>/', login_required(close_spot_signal), name='close_spot_signal'),
    path('signals/spot/add-target/', login_required(add_spot_target), name='add_spot_target'),
    path('signals/spot/add-news/', login_required(add_spot_news), name='add_spot_news'),
    path('signals/spot/add/', login_required(add_spot_signal), name='add_spot_signal'),
    path('gifts/user-list/', UserListGifts.as_view(), name='gifst_user_list'),
    path('gifts/user/<int:user_id>/detail/', user_gifts_detail, name='user_gifst_detail'),
    path('gifts/deactive/<int:gift_id>/', deactive_user_gift, name='deactive_user_gift'),
    path('gifts/active/<int:gift_id>/', active_user_gift, name='active_user_gift'),
    path('gifts/add/', add_gift, name='add_gift'),
    path('cash-withdrawals/', CashWithdrawalList.as_view(), name='cash_withdrawal_list'),
    path('cash-withdrawals/confirm/<id>', confirm_cash_withdrawal, name='confirm_cash_withdrawal'),
    path('cash-withdrawals/delete/<id>', delete_cash_withdrawal, name='delete_cash_withdrawal'),
    path('login', admin_login, name='admin_login'),

]
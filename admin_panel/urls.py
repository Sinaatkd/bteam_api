from django.urls import path

from django.contrib.auth.decorators import login_required

from admin_panel.views.story_views import *
from .views.auth_view import admin_login
from .views.cash_withdrawal_view import *
from .views.financial_view import *
from .views.news_view import *
from .views.special_account_view import *
from .views.spot_signal_view import *
from .views.gift_view import UsersList as UserListGifts 
from .views.gift_view import *
from .views.futures_signal_view import *
from .views.transaction_view import *
from .views.user_views import *
from .views.copy_trade_view import *

urlpatterns = [
    path('', login_required(home_page), name='home'),
    path('users/', login_required(UsersList.as_view()), name='users_list'),
    path('users-full-auth/', login_required(UsersFullAuthList.as_view()), name='users_has_requested_full_auth_list'),
    path('unconfirm-full-auth/<user_id>', login_required(unconfirm_full_auth), name='unconfirm_full_auth'),
    path('confirm-full-auth/<user_id>', login_required(confirm_full_auth), name='confirm_full_auth'),

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
    path('news/add-new/', login_required(CreateNews.as_view()), name='add_new'),
    path('news/edit/<int:pk>/', login_required(UpdateNews.as_view()), name='edit_new'),
    path('news/delete/<news_id>/', login_required(delete_news), name='delete_news'),

    path('news-categories', login_required(NewsCategoriesList.as_view()), name='news_categories_list'),
    path('news-categories/add-new/', login_required(CreateNewsCategory.as_view()), name='add_news_category'),
    path('news-categories/edit/<int:pk>/', login_required(UpdateNewsCategory.as_view()), name='edit_news_category'),
    path('news-categories/delete/<news_category_id>/', login_required(delete_news_category), name='delete_news_category'),
    
    path('special-account-item/', login_required(SpecialAccountItemList.as_view()), name='special_account_item_list'),
    path('special-account-item/add-new/', login_required(add_special_account), name='special_account_new'),
    path('special-account-item/delete/<special_account_id>/', login_required(delete_special_account), name='delete_special_account'),
    path('signals/futures/', login_required(FuturesSignalsList.as_view()), name='signal_futures_list'),
    path('signals/futures/detail/<futures_id>/', login_required(detail_futures), name='detail_futures'),
    path('signals/futures/delete/<futures_id>/', login_required(delete_futures_signal), name='delete_futures_signal'),
    path('signals/futures/close/<futures_id>/', login_required(close_futures_signal), name='close_futures_signal'),
    path('signals/futures/add-target/', login_required(add_futures_target), name='add_futures_target'),
    path('signals/futures/add-news/', login_required(add_futures_news), name='add_futures_news'),
    path('signals/futures/add-alarm/', login_required(add_futures_alarm), name='add_futures_alarm'),
    path('signals/delete-alarm/<alarm_id>/', login_required(delete_futures_alarm), name='delete_alarm'),
    path('signals/futures/add/', login_required(add_futures_signal), name='add_futures_signal'),
    path('signals/spot/', login_required(SpotSignalsList.as_view()), name='signal_spot_list'),
    path('signals/spot/detail/<spot_id>/', login_required(detail_spot), name='detail_spot'),
    path('signals/spot/delete/<spot_id>/', login_required(delete_spot_signal), name='delete_spot_signal'),
    path('signals/spot/close/<spot_id>/', login_required(close_spot_signal), name='close_spot_signal'),
    path('signals/spot/add-target/', login_required(add_spot_target), name='add_spot_target'),
    path('signals/spot/add-news/', login_required(add_spot_news), name='add_spot_news'),
    path('signals/spot/add-alarm/', login_required(add_spot_alarm), name='add_spot_alarm'),
    path('signals/spot/add/', login_required(add_spot_signal), name='add_spot_signal'),
    
    path('gifts/user-list/', login_required(UserListGifts.as_view()), name='gifst_user_list'),
    path('gifts/user/<int:user_id>/detail/', login_required(user_gifts_detail), name='user_gifst_detail'),
    path('gifts/deactive/<int:gift_id>/', login_required(deactive_user_gift), name='deactive_user_gift'),
    path('gifts/active/<int:gift_id>/', login_required(active_user_gift), name='active_user_gift'),
    path('gifts/add/', login_required(add_gift), name='add_gift'),
    
    path('cash-withdrawals/', login_required(CashWithdrawalList.as_view()), name='cash_withdrawal_list'),
    path('cash-withdrawals/confirm/<id>', login_required(confirm_cash_withdrawal), name='confirm_cash_withdrawal'),
    path('cash-withdrawals/delete/<id>', login_required(delete_cash_withdrawal), name='delete_cash_withdrawal'),
    path('cash-withdrawals/edit-wallet/', login_required(edit_wallet), name='edit_wallet'),
    path('finanical-statistics/', login_required(finanical_statistics), name='financial_statistics'),
    
    path('baskets', BasketsList.as_view(), name='baskets'),
    path('baskets/new', CreateBasket.as_view(), name='create_basket'),
    path('baskets/<int:pk>/detial', DetailBasket.as_view(), name='detail_basket'),
    path('baskets/<int:pk>/delete', delete_basket, name='delete_basket'),
    path('baskets/<int:pk>/edit', BasketEdit.as_view(), name='edit_basket'),
    path('baskets/<int:pk>/disabled-accept-participant', disabled_accept_participant, name='disabled_accept_participant'),
    path('baskets/<int:pk>/apply-orders-for-participants', apply_order_for_participants, name='apply_order_for_participants'),
    path('baskets/<int:pk>/set-stage', set_stage, name='set_stage'),
    path('baskets/<int:pk>/freeze', freeze_basket, name='freeze_basket'),
    path('baskets/<int:pk>/deactive', deactive_basket, name='deactive_basket'),
    path('baskets/<int:pk>/cancel-orders', cancel_orders, name='cancel_orders'),
    path('baskets/<int:pk>/sell-orders', sell_orders, name='sell_orders'),
    path('baskets/set-tp-sl', set_tp_sl, name='set_tp_sl'),
    
    path('stories', login_required(StoryList.as_view()), name='stories_list'),
    path('stories/new', login_required(CreateStory.as_view()), name='create_story'),
    path('stories/delete-story/<int:pk>', login_required(delete_story), name='delete_story'),
    
    path('login', admin_login, name='admin_login'),

]
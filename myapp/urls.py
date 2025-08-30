from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('wallet/<int:user_id>/', views.wallet_view, name='wallet'),

    # Later you’ll add these:
    # path('holdings/<int:user_id>/', views.holdings_view, name='holdings'),
    # path('trades/<int:user_id>/', views.trades_view, name='trades'),
]

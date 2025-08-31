from django.urls import path
from . import views

urlpatterns = [
    path("api/signup/", views.signup),
    path("api/login/", views.login),
    path("api/wallet/<int:user_id>/", views.wallet_view),
    path("api/holdings/<int:user_id>/", views.holdings_view),
    path("api/trade/<int:user_id>/", views.trade_view),
  
    path("api/prices/", views.crypto_prices, name="crypto-prices"),
    path("api/candles/<str:symbol>/", views.crypto_candles, name="crypto-candles"),
]
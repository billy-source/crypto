from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("wallet/", views.wallet_view, name="wallet"),
    path("holdings/", views.holdings_view, name="holdings"),
    path("trades/", views.trades_view, name="trades"),
    path("trade/", views.place_trade, name="place_trade"),
]

from django.urls import path
from . import views

urlpatterns = [
    # --------------------
    # Template Pages
    # --------------------
    path("signup/", views.signup_page, name="signup_page"),
    path("login/", views.login_page, name="login_page"),
    path("dashboard/", views.dashboard_page, name="dashboard_page"),
    path("trade/", views.trade_page, name="trade_page"),

    # --------------------
    # API Endpoints
    # --------------------
    path("api/signup/", views.signup_view, name="api_signup"),
    path("api/login/", views.login_view, name="api_login"),
    path("api/logout/", views.logout_view, name="api_logout"),
    path("api/dashboard/", views.dashboard_view, name="api_dashboard"),
    path("api/trade/", views.place_trade, name="api_trade"),
]

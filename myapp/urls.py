from django.urls import path
from . import views

urlpatterns = [
   
    path("login/", views.render_login_page, name="login"),
    path("signup/", views.render_signup_page, name="signup"),
    path("beginner-dashboard/", views.render_beginner_dashboard, name="beginner_dashboard"),
    path("trade/", views.render_trade_page, name="trade"),
    path("price-page/", views.render_price_page, name="price-page"),

   
    path("api/login/", views.login_view, name="api_login"),
    path("api/signup/", views.signup_view, name="api_signup"),
    path("api/logout/", views.logout_view, name="api_logout"),    
   
    path("api/beginner-dashboard/", views.beginner_dashboard, name="api_beginner_dashboard"),
    path("api/trade/", views.place_trade, name="api_trade"),
]

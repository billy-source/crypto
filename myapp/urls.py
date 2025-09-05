from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),                 # Home page
    path("signup/", views.signup_view, name="signup"),      # Signup page
    path("login/", views.login_view, name="login"),         # Login page
    path("logout/", views.logout_view, name="logout"),      # Logout
    path("dashboard/", views.dashboard_view, name="dashboard"),  # User dashboard
    path("trade/", views.trade_view, name="trade"),         # Trade page
    path("trade/", views.trade_view, name="trade"),
 # Process trade form
]

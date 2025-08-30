from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('wallet/<int:user_id>/', views.wallet_view, name='wallet'),
]

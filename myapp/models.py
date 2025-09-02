from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=100000.00)
    currency = models.CharField(max_length=10, default="USD")

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="holdings")
    crypto_symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)

class Trade(models.Model):
    TRADE_CHOICES = [("BUY", "Buy"), ("SELL", "Sell")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trades")
    crypto_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=4, choices=TRADE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

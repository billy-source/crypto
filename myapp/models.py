from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("100000.00"))

    def __str__(self):
        return f"{self.user.username} Wallet - Balance: {self.balance}"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="holdings")
    crypto_symbol = models.CharField(max_length=10)  # e.g. BTC, ETH
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal("0"))

    class Meta:
        unique_together = ("user", "crypto_symbol")

    def __str__(self):
        return f"{self.user.username} holds {self.amount} {self.crypto_symbol}"


class Trade(models.Model):
    TRADE_TYPES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trades")
    crypto_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=15, decimal_places=2)  # price per unit
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)  # amount * price
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.trade_type} {self.amount} {self.crypto_symbol} @ {self.price}"

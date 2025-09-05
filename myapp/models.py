from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.crypto_symbol}: {self.amount}"


class Trade(models.Model):
    TRADE_TYPES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.trade_type} {self.amount} {self.crypto_symbol}"

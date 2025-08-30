from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)   # Beginner = False, Pro = True
    cash_balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('10000.00'))  # starting demo cash

    def __str__(self):
        return f"{self.user.username} - {'Pro' if self.is_pro else 'Beginner'}"



class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)  # e.g., BTC, ETH
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return f"{self.user.username} holds {self.amount} {self.symbol}"



class Trade(models.Model):
    TRADE_TYPE_CHOICES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)  # e.g., BTC
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=20, decimal_places=2)   # simulated price
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.trade_type} {self.quantity} {self.symbol} at {self.price}"



class PriceHistory(models.Model):
    symbol = models.CharField(max_length=10)   # e.g., BTC, ETH
    price = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.price} at {self.timestamp}"

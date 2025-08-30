from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)  # Beginner by default
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000.00)  # $100,000 for beginners
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Pro' if self.is_pro else 'Beginner'}"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    average_price = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.user.username} holds {self.amount} {self.symbol}"


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    side = models.CharField(max_length=4, choices=[("BUY", "Buy"), ("SELL", "Sell")])
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.side} {self.amount} {self.symbol} @ {self.price}"


class PriceHistory(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} @ {self.price} ({self.timestamp})"

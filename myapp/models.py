from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)  # beginner = False, pro = True

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default="USD")  # Can set to KES for Mpesa

    def __str__(self):
        return f"{self.user.username} Wallet - {self.balance} {self.currency}"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.crypto_symbol} ({self.amount})"


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=4, choices=(("BUY", "Buy"), ("SELL", "Sell")))
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)  # ✅ add this
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.trade_type} {self.crypto_symbol}"


class PriceHistory(models.Model):
    crypto_symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto_symbol} - {self.price} @ {self.timestamp}"

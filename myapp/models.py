from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_virtual = models.BooleanField(default=True)  # Beginner wallet

    def __str__(self):
        return f"{self.user.username} - ${self.balance}"

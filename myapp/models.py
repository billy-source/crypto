from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000.00)
    is_virtual = models.BooleanField(default=True)  # True = beginner/virtual, False = pro

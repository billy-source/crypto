from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Holding, Trade

# ---- User ----
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

# ---- Wallet ----
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance", "currency"]

# ---- Holding ----
class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ["id", "crypto_symbol", "amount"]

# ---- Trade (response) ----
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["id", "crypto_symbol", "trade_type", "amount", "price", "total_cost", "timestamp"]

# ---------- Request serializers (validation) ----------
class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TradeRequestSerializer(serializers.Serializer):
    trade_type = serializers.ChoiceField(choices=["BUY", "SELL"])
    crypto_symbol = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)


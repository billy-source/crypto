from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Holding, Trade


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# Signup Serializer
class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Wallet Serializer
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance"]


# Holding Serializer
class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ["id", "crypto_symbol", "amount"]


# Trade Serializer
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["id", "crypto_symbol", "trade_type", "amount", "price", "total_cost", "timestamp"]


# Trade Request Serializer (for API requests)
class TradeRequestSerializer(serializers.Serializer):
    trade_type = serializers.ChoiceField(choices=["BUY", "SELL"])
    crypto_symbol = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=15, decimal_places=2)

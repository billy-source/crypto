from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Holding, Trade

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance"]

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ["crypto_symbol", "amount"]

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["crypto_symbol", "trade_type", "amount", "price", "total_cost", "timestamp"]

class TradeRequestSerializer(serializers.Serializer):
    trade_type = serializers.ChoiceField(choices=["BUY", "SELL"])
    crypto_symbol = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)

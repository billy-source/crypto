from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Holding, Trade

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance", "currency"]

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ["id", "crypto_symbol", "amount"]

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["id", "crypto_symbol", "trade_type", "amount", "price", "total_cost", "timestamp"]

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

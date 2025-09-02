from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
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
        fields = [
            "id",
            "crypto_symbol",
            "trade_type",
            "amount",
            "price",
            "total_cost",
            "timestamp",
        ]


# ---- Signup ----
class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_password(self, value):
        """Use Django’s built-in password validators."""
        validate_password(value)
        return value


# ---- Login ----
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# ---- Trade Request ----
class TradeRequestSerializer(serializers.Serializer):
    trade_type = serializers.ChoiceField(choices=["BUY", "SELL"])
    crypto_symbol = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


# ---- Dashboard/Profile (Combined User + Wallet + Holdings + Trades) ----
class UserDashboardSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)
    holdings = HoldingSerializer(many=True, read_only=True)
    trades = TradeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "wallet", "holdings", "trades"]

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Holding, Trade



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'is_virtual']


class HoldingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Holding
        fields = ['id', 'user', 'crypto', 'amount']



class TradeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Trade
        fields = ['id', 'user', 'crypto', 'trade_type', 'amount', 'price', 'timestamp']

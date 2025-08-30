from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        # Create wallet with $100,000 virtual balance
        Wallet.objects.create(user=user, balance=100000.00, is_virtual=True)
        return user

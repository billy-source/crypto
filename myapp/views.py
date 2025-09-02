from decimal import Decimal, InvalidOperation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Wallet, Holding, Trade
from .serializers import (
    UserSerializer,
    WalletSerializer,
    HoldingSerializer,
    TradeSerializer,
    SignupSerializer,
    LoginSerializer,
    TradeRequestSerializer,
    UserDashboardSerializer,
)


# ---- Signup ----
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        email = serializer.validated_data.get("email", "")
        password = serializer.validated_data["password"]

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        Wallet.objects.create(user=user, balance=Decimal("10000.00"))  # give new users starting balance

        return Response({"message": "User created successfully"}, status=201)

    return Response(serializer.errors, status=400)


# ---- Login ----
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Django session login
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=400)
    return Response(serializer.errors, status=400)


# ---- Logout ----
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out successfully"})


# ---- Dashboard ----
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """Return combined User + Wallet + Holdings + Trades"""
    serializer = UserDashboardSerializer(request.user)
    return Response(serializer.data)


# ---- Trade ----
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def trade_view(request):
    serializer = TradeRequestSerializer(data=request.data)
    if serializer.is_valid():
        trade_type = serializer.validated_data["trade_type"]
        crypto_symbol = serializer.validated_data["crypto_symbol"].upper()
        amount = serializer.validated_data["amount"]
        price = serializer.validated_data["price"]

        wallet = request.user.wallet
        total_cost = amount * price

        if trade_type == "BUY":
            if wallet.balance < total_cost:
                return Response({"error": "Insufficient balance"}, status=400)
            wallet.balance -= total_cost
            wallet.save()

            holding, _ = Holding.objects.get_or_create(user=request.user, crypto_symbol=crypto_symbol)
            holding.amount += amount
            holding.save()

        elif trade_type == "SELL":
            holding = Holding.objects.filter(user=request.user, crypto_symbol=crypto_symbol).first()
            if not holding or holding.amount < amount:
                return Response({"error": "Not enough holdings to sell"}, status=400)
            holding.amount -= amount
            holding.save()
            wallet.balance += total_cost
            wallet.save()

        trade = Trade.objects.create(
            user=request.user,
            crypto_symbol=crypto_symbol,
            trade_type=trade_type,
            amount=amount,
            price=price,
            total_cost=total_cost,
        )

        return Response(TradeSerializer(trade).data, status=201)

    return Response(serializer.errors, status=400)

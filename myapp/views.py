from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Wallet, Holding, Trade
from .serializers import (
    SignupSerializer, LoginSerializer, WalletSerializer,
    HoldingSerializer, TradeSerializer, TradeRequestSerializer, UserSerializer
)

# -------------------------
# API SECTION (Existing Code)
# -------------------------

def get_real_time_price(crypto_symbol):
    prices = {
        "BTC": 60000.00,
        "ETH": 4000.00,
        "SOL": 200.00,
    }
    return prices.get(crypto_symbol.upper(), 0)

@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        Wallet.objects.create(user=user, balance=100000.00)  # starting balance
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "Signup successful", "token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({"message": "Logged out successfully"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user, defaults={"balance": 100000})
    holdings = Holding.objects.filter(user=request.user)
    trades = Trade.objects.filter(user=request.user).order_by("-timestamp")

    return Response({
        "user": UserSerializer(request.user).data,
        "wallet": WalletSerializer(wallet).data,
        "holdings": HoldingSerializer(holdings, many=True).data,
        "trades": TradeSerializer(trades, many=True).data,
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def place_trade(request):
    serializer = TradeRequestSerializer(data=request.data)
    if serializer.is_valid():
        trade_type = serializer.validated_data["trade_type"]
        crypto_symbol = serializer.validated_data["crypto_symbol"].upper()
        amount = serializer.validated_data["amount"]

        price = get_real_time_price(crypto_symbol)
        if price == 0:
            return Response({"error": "Invalid crypto symbol"}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = amount * Decimal(price)
        wallet, _ = Wallet.objects.get_or_create(user=request.user, defaults={"balance": 100000})

        if trade_type == "BUY":
            if wallet.balance < total_cost:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            wallet.balance -= total_cost
            wallet.save()
            holding, _ = Holding.objects.get_or_create(user=request.user, crypto_symbol=crypto_symbol)
            holding.amount += amount
            holding.save()

        elif trade_type == "SELL":
            holding = Holding.objects.filter(user=request.user, crypto_symbol=crypto_symbol).first()
            if not holding or holding.amount < amount:
                return Response({"error": "Not enough holdings to sell"}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response(TradeSerializer(trade).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# TEMPLATE SECTION (NEW)
# -------------------------

def signup_page(request):
    return render(request, "signup.html")

def login_page(request):
    return render(request, "login.html")

@login_required
def dashboard_page(request):
    wallet = Wallet.objects.get(user=request.user)
    holdings = Holding.objects.filter(user=request.user)
    trades = Trade.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "dashboard.html", {
        "wallet": wallet,
        "holdings": holdings,
        "trades": trades
    })

@login_required
def trade_page(request):
    return render(request, "trade.html")

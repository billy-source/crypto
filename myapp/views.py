from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Wallet, Holding, Trade
from .serializers import (
    SignupSerializer, LoginSerializer, WalletSerializer,
    HoldingSerializer, TradeSerializer, TradeRequestSerializer, UserSerializer
)

# -------------------------
# Utility: Dummy Price Fetcher
# -------------------------
def get_real_time_price(crypto_symbol):
    prices = {
        "BTC": 60000.00,
        "ETH": 4000.00,
        "SOL": 200.00,
    }
    return prices.get(crypto_symbol.upper(), 0)

# -------------------------
# 1. Home Page
# -------------------------
def home_view(request):
    return render(request, "home.html")

# -------------------------
# 2. Signup View
# -------------------------
@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def signup_view(request):
    if request.method == "POST":
        serializer = SignupSerializer(data=request.data if request.content_type == "application/json" else request.POST)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)
            Wallet.objects.create(user=user, balance=100000.00)  # starting balance
            token, _ = Token.objects.get_or_create(user=user)

            if request.content_type == "application/json":  # Postman
                return Response({"message": "Signup successful", "token": token.key}, status=status.HTTP_201_CREATED)
            else:  # Browser
                return redirect("login")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return render(request, "signup.html")

# -------------------------
# 3. Login View
# -------------------------
@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data if request.content_type == "application/json" else request.POST)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)  # session-based login
                token, _ = Token.objects.get_or_create(user=user)
                if request.content_type == "application/json":
                    return Response({"message": "Login successful", "token": token.key})
                else:
                    return redirect("dashboard")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    return render(request, "login.html")

# -------------------------
# 4. Logout
# -------------------------
def logout_view(request):
    if request.user.is_authenticated:
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
    return redirect("home")

# -------------------------
# 5. Dashboard View
# -------------------------
@login_required
def dashboard_view(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user, defaults={"balance": 100000})
    holdings = Holding.objects.filter(user=request.user)
    trades = Trade.objects.filter(user=request.user).order_by("-timestamp")

    if request.headers.get("Content-Type") == "application/json":
        return Response({
            "user": UserSerializer(request.user).data,
            "wallet": WalletSerializer(wallet).data,
            "holdings": HoldingSerializer(holdings, many=True).data,
            "trades": TradeSerializer(trades, many=True).data,
        })

    return render(request, "dashboard.html", {
        "wallet": wallet,
        "holdings": holdings,
        "trades": trades,
    })

# -------------------------
# 6. Trade View (Form + API)
# -------------------------
@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def trade_view(request):
    if request.method == "POST":
        serializer = TradeRequestSerializer(data=request.data if request.content_type == "application/json" else request.POST)
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

            if request.content_type == "application/json":
                return Response(TradeSerializer(trade).data, status=status.HTTP_201_CREATED)
            else:
                return redirect("dashboard")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return render(request, "trade.html")

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from .models import Wallet, Holding, Trade
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    WalletSerializer,
    HoldingSerializer,
    TradeSerializer,
    TradeRequestSerializer,
    UserSerializer,
)



def render_homepage(request):
    """
    Renders the main home.html template for the homepage.
    """
    return render(request, 'home.html')

def render_login_page(request):
    """
    Renders the login.html template.
    """
    return render(request, 'login.html')

def render_signup_page(request):
    """
    Renders the signup.html template.
    """
    return render(request, 'signup.html')

def render_beginner_dashboard(request):
    """
    Renders the beginner_dashboard.html template.
    """
    return render(request, 'beginner_dashboard.html')

def render_trade_page(request):
    """
    Renders the trade.html template.
    """
    return render(request, 'trade.html')

def render_price_page(request):
    """
    Renders the price.html template.
    """
    return render(request, 'price.html')




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
        
        Wallet.objects.create(user=user, balance=100000.00)

        return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out successfully"})




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def beginner_dashboard(request):
    """Show wallet, holdings, and trades"""
    wallet = Wallet.objects.get(user=request.user)
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
    """Place a BUY or SELL trade"""
    serializer = TradeRequestSerializer(data=request.data)
    if serializer.is_valid():
        trade_type = serializer.validated_data["trade_type"]
        crypto_symbol = serializer.validated_data["crypto_symbol"].upper()
        amount = serializer.validated_data["amount"]
        price = serializer.validated_data["price"]
        total_cost = amount * price

        wallet = Wallet.objects.get(user=request.user)

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

from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet, Holding, Trade
from .serializers import WalletSerializer, HoldingSerializer, TradeSerializer, SignupSerializer

# ---- Signup ----
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        email = serializer.validated_data.get("email", "")
        password = serializer.validated_data["password"]
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        Wallet.objects.create(user=user, balance=100000.00)  # give $100k
        return Response({"message": "User created successfully"}, status=201)
    return Response(serializer.errors, status=400)

# ---- Login ----
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({"message": "Login successful"})
    return Response({"error": "Invalid credentials"}, status=400)

# ---- Wallet ----
@api_view(["GET"])
def wallet_view(request):
    wallet = request.user.wallet
    return Response(WalletSerializer(wallet).data)

# ---- Holdings ----
@api_view(["GET"])
def holdings_view(request):
    holdings = Holding.objects.filter(user=request.user)
    return Response(HoldingSerializer(holdings, many=True).data)

# ---- Trades ----
@api_view(["GET"])
def trades_view(request):
    trades = Trade.objects.filter(user=request.user).order_by("-timestamp")
    return Response(TradeSerializer(trades, many=True).data)

# ---- Place Trade ----
@api_view(["POST"])
def place_trade(request):
    trade_type = request.data.get("trade_type")
    crypto_symbol = request.data.get("crypto_symbol")
    amount = Decimal(request.data.get("amount"))
    price = Decimal(request.data.get("price"))
    total_cost = amount * price
    wallet = request.user.wallet

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
            return Response({"error": "Insufficient holdings"}, status=400)
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

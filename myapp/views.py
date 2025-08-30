from decimal import Decimal, InvalidOperation
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

# If you use JWT:
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Wallet, Holding, Trade
from .serializers import (
    UserSerializer,
    WalletSerializer,
    HoldingSerializer,
    TradeSerializer,
    SignupSerializer,
    LoginSerializer,
    TradeRequestSerializer,
)

# -------- helper: JWT tokens --------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}

# -------------------- SIGNUP --------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    s = SignupSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    username = s.validated_data.get("username")
    email = s.validated_data.get("email")
    password = s.validated_data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    # NOTE: your Wallet model has no `is_virtual`, so don't pass it.
    Wallet.objects.create(user=user, balance=Decimal("100000.00"))  # currency defaults to "USD"

    tokens = get_tokens_for_user(user)
    return Response(
        {"message": "Account created successfully!", "user": UserSerializer(user).data, "tokens": tokens},
        status=201,
    )

# -------------------- LOGIN --------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    s = LoginSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    username = s.validated_data.get("username")
    password = s.validated_data.get("password")

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    tokens = get_tokens_for_user(user)
    return Response({"message": "Login successful", "user": UserSerializer(user).data, "tokens": tokens}, status=200)

# -------------------- WALLET --------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wallet_view(request, user_id):
    if request.user.id != user_id:
        return Response({"error": "You can only view your own wallet"}, status=403)

    wallet = get_object_or_404(Wallet, user_id=user_id)
    return Response(WalletSerializer(wallet).data, status=200)

# -------------------- HOLDINGS --------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def holdings_view(request, user_id):
    if request.user.id != user_id:
        return Response({"error": "You can only view your own holdings"}, status=403)

    holdings = Holding.objects.filter(user_id=user_id)
    return Response(HoldingSerializer(holdings, many=True).data, status=200)

# -------------------- TRADE (BUY/SELL) --------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def trade_view(request, user_id):
    if request.user.id != user_id:
        return Response({"error": "You can only trade from your own account"}, status=403)

    req = TradeRequestSerializer(data=request.data)
    req.is_valid(raise_exception=True)

    trade_type = req.validated_data["trade_type"]
    crypto_symbol = req.validated_data["crypto_symbol"]
    amount = req.validated_data["amount"]
    price = req.validated_data["price"]

    # make sure positive
    if amount <= 0 or price <= 0:
        return Response({"error": "amount and price must be > 0"}, status=400)

    wallet = get_object_or_404(Wallet, user_id=user_id)
    total_cost = (amount * price).quantize(Decimal("0.01"))

    if trade_type == "BUY":
        if wallet.balance < total_cost:
            return Response({"error": "Insufficient balance"}, status=400)
        wallet.balance = (wallet.balance - total_cost).quantize(Decimal("0.01"))
        wallet.save()

        holding, _ = Holding.objects.get_or_create(user=request.user, crypto_symbol=crypto_symbol)
        holding.amount = (holding.amount + amount)
        holding.save()

    elif trade_type == "SELL":
        try:
            holding = Holding.objects.get(user=request.user, crypto_symbol=crypto_symbol)
        except Holding.DoesNotExist:
            return Response({"error": "You do not own this crypto"}, status=400)

        if holding.amount < amount:
            return Response({"error": "Not enough holdings to sell"}, status=400)

        holding.amount = (holding.amount - amount)
        holding.save()

        wallet.balance = (wallet.balance + total_cost).quantize(Decimal("0.01"))
        wallet.save()

    # Save trade with total_cost
    trade = Trade.objects.create(
        user=request.user,
        crypto_symbol=crypto_symbol,
        trade_type=trade_type,
        amount=amount,
        price=price,
        total_cost=total_cost,
    )

    return Response(
        {
            "message": f"{trade_type} {amount} {crypto_symbol} @ {price} successful",
            "wallet_balance": str(wallet.balance),
            "trade": TradeSerializer(trade).data,
        },
        status=201,
    )

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Wallet
from .serializers import UserSerializer, WalletSerializer


# -------------------- SIGNUP --------------------
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    # Create wallet with virtual money
    Wallet.objects.create(user=user, balance=100000.00, is_virtual=True)

    # Generate token for API authentication
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Account created successfully!",
        "user": UserSerializer(user).data,
        "token": token.key
    })


# -------------------- LOGIN --------------------
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    # Generate token
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Login successful",
        "user": UserSerializer(user).data,
        "token": token.key
    })


# -------------------- WALLET VIEW --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_view(request, user_id):
    try:
        if request.user.id != user_id:
            return Response({"error": "You can only view your own wallet"}, status=403)

        wallet = Wallet.objects.get(user_id=user_id)
        return Response(WalletSerializer(wallet).data)
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet not found"}, status=404)

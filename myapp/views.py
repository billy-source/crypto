from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Wallet
from .serializers import UserSerializer, WalletSerializer

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    # Create wallet with $100,000
    Wallet.objects.create(user=user, balance=100000.00, is_virtual=True)

    return Response({
        "message": "Account created successfully!",
        "user": UserSerializer(user).data
    })

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    return Response({
        "message": "Login successful",
        "user": UserSerializer(user).data
    })

@api_view(['GET'])
def wallet_view(request, user_id):
    try:
        wallet = Wallet.objects.get(user_id=user_id)
        return Response(WalletSerializer(wallet).data)
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet not found"}, status=404)

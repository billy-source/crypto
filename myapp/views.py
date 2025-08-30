from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Wallet
from .serializers import UserSerializer, WalletSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

   
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

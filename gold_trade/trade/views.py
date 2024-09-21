import redis
import requests
from threading import Lock
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import status



from .models import Transaction
from .serializers import UserSerializer, TransactionSerializer
User = get_user_model()

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_gold_price():
    gold_price = redis_instance.get('gold_price')
    if gold_price is None:
        response = requests.get('https://api.metalpriceapi.com/v1/latest?access_key=YOUR_API_KEY')
        gold_price = response.json().get('rates', {}).get('XAU')
        redis_instance.set('gold_price', gold_price, ex=300)  
    return float(gold_price)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
class GoldPriceView(APIView):
    def get(self, request):
        price = get_gold_price()
        return Response({'gold_price': price})

transaction_lock = Lock()

class BuySellGoldView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        transaction_type = request.data.get('transaction_type')
        gold_grams = float(request.data.get('gold_grams'))

        price_per_gram = get_gold_price()
        total_price = gold_grams * price_per_gram

        with transaction_lock:
            try:
                if transaction_type == 'BUY':
                    pass  # TODO: 
                elif transaction_type == 'SELL':
                    pass  # TODO: 

                transaction = Transaction.objects.create(
                    user=request.user,
                    transaction_type=transaction_type,
                    gold_grams=gold_grams,
                    price_per_gram=price_per_gram,
                    total_price=total_price
                )
                return Response({'message': f'{transaction_type} transaction successful'}, status=200)
            except Exception as e:
                return Response({'error': str(e)}, status=400)

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)

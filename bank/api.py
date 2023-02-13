from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from decimal import Decimal

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer


from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer

    @action(detail=True, methods=['post',])
    def make_deposit_or_withdrawal(self, request):
        requestData = request.data

        accountId = requestData.pop('account')
        data = {
            **requestData,
            "accounts": [accountId]
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # update account amount
            account = Account.objects.filter(id=accountId).first()
            if requestData['transaction_type'] == 'Deposit':
                account.amount += requestData['amount']

            if requestData['transaction_type'] == 'Withdrawal':
                account.amount -= requestData['amount']

            Account.objects.filter(id=accountId).update(amount=account.amount)

            serializer.save()
            return Response({'message': 'Transaction completed successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post',])
    def make_transfer(self, request):
        requestData = request.data
        senderAccountId = requestData.pop('sender_account')
        receiverAccountId = requestData.pop('receiver_account')
        data = {
            **requestData,
            "accounts": [senderAccountId, receiverAccountId],
            "transaction_type": "Transfer"
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # update accounts amount
            senderAccount = Account.objects.filter(id=senderAccountId).first()
            senderAccount.amount -= requestData['amount']
            Account.objects.filter(id=senderAccountId).update(
                amount=senderAccount.amount)

            receiverAccount = Account.objects.filter(
                id=receiverAccountId).first()
            receiverAccount.amount += requestData['amount']
            Account.objects.filter(id=receiverAccountId).update(
                amount=receiverAccount.amount)

            serializer.save()
            return Response({'message': 'Transfer completed successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

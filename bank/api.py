from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .utils import modifyAccountAmount


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
            "accountsId": [accountId]
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # update account amount
            account = Account.objects.filter(id=accountId).first()
            newAmount = modifyAccountAmount(
                account.amount, requestData['amount'], requestData['transaction_type'])
            accountSerializer = AccountSerializer(
                account, data={'amount': newAmount}, partial=True)

            if accountSerializer.is_valid():
                serializer.save()
                accountSerializer.save()
                return Response({'message': 'Transaction completed successfully!', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(accountSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post',])
    def make_transfer(self, request):
        requestData = request.data
        senderAccountId = requestData.pop('sender_account')
        receiverAccountId = requestData.pop('receiver_account')
        data = {
            **requestData,
            "accountsId": [senderAccountId, receiverAccountId],
            "transaction_type": "Transfer"
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # update accounts amount
            senderAccount = Account.objects.filter(id=senderAccountId).first()
            newSenderAccountAmount = modifyAccountAmount(
                senderAccount.amount, requestData['amount'], 'Withdrawal')
            senderAccountSerializer = AccountSerializer(
                senderAccount, data={'amount': newSenderAccountAmount}, partial=True)

            receiverAccount = Account.objects.filter(
                id=receiverAccountId).first()
            newReceiverAccountAmount = modifyAccountAmount(
                receiverAccount.amount, requestData['amount'], 'Deposit')
            receiverAccountSerializer = AccountSerializer(
                receiverAccount, data={'amount': newReceiverAccountAmount}, partial=True)

            if senderAccountSerializer.is_valid():
                if receiverAccountSerializer.is_valid():
                    serializer.save()
                    senderAccountSerializer.save()
                    receiverAccountSerializer.save()
                    return Response({'message': 'Transfer completed successfully!', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
                return Response(receiverAccountSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(senderAccountSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

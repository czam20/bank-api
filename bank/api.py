from django.db import transaction
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .utils import modifyAccountAmount
from persons.models import Person


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    @action(detail=True, methods=['get'])
    def get_accounts_by_user(self, request, user_dni):
        try:
            user = Person.objects.get(dni=user_dni)
            print(user.id)
            if user:
                queryset = self.filter_queryset(
                    Account.objects.filter(person=user.id))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    @action(detail=True, methods=['get'])
    def get_transactions_by_account(self, request, account_id):
        try:
            account = Account.objects.filter(id=account_id)
            if account:
                queryset = Transaction.objects.filter(accounts=account_id)
                serializer = self.serializer_class(queryset, many=True)
                return Response({'transactions': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def get_transactions_by_type(self, request, type):
        queryset = Transaction.objects.filter(transaction_type=type)
        serializer = self.serializer_class(queryset, many=True)
        return Response({'transactions': serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def make_deposit_or_withdrawal(self, request):
        requestData = request.data
        accountId = requestData.pop('account')
        data = {
            **requestData,
            'amount': requestData['amount']*(-1) if requestData['transaction_type'] == 'Withdrawal' else requestData['amount'],
            "accountsId": [accountId]
        }
        serializer = self.serializer_class(data=data)
        account = Account.objects.select_for_update().filter(id=accountId).first()

        with transaction.atomic():
            if serializer.is_valid():
                # update account amount 
                newAmount = modifyAccountAmount(
                    account.amount, requestData['amount'], requestData['transaction_type'])
                account.amount = newAmount
                account.save()
                serializer.save()
                return Response({'message': 'Transaction completed successfully!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def make_deposit_or_withdrawal(self, request):
    #     requestData = request.data

    #     accountId = requestData.pop('account')
    #     data = {
    #         **requestData,
    #         "accountsId": [accountId]
    #     }

    #     serializer = self.serializer_class(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Transaction completed successfully!', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    @action(detail=True, methods=['post'])
    def make_transfer(self, request):
        requestData = request.data
        senderAccountId = requestData.pop('sender_account')
        receiverAccountId = requestData.pop('receiver_account')
        data = {
            **requestData,
            "accountsId": [senderAccountId, receiverAccountId],
            "transaction_type": "Transfer"
        }
        senderAccount = Account.objects.filter(id=senderAccountId).select_for_update().first()
        receiverAccount = Account.objects.select_for_update().filter(id=receiverAccountId).first()
        
        serializer = self.serializer_class(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # update accounts amount
                newSenderAccountAmount = modifyAccountAmount(
                    senderAccount.amount, requestData['amount'], 'Withdrawal')
                senderAccount.amount = newSenderAccountAmount
                senderAccount.save()

                newReceiverAccountAmount = modifyAccountAmount(
                    receiverAccount.amount, requestData['amount'], 'Deposit')
                receiverAccount.amount = newReceiverAccountAmount
                receiverAccount.save()
                serializer.save()
                return Response({'message': 'Transfer completed successfully!', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def make_transfer(self, request):
    #     requestData = request.data
    #     senderAccountId = requestData.pop('sender_account')
    #     receiverAccountId = requestData.pop('receiver_account')
    #     data = {
    #         **requestData,
    #         "accountsId": [senderAccountId, receiverAccountId],
    #         "transaction_type": "Transfer"
    #     }

    #     serializer = self.serializer_class(data=data)
    #     if serializer.is_valid():

    #         serializer.save()

    #         return Response({'message': 'Transfer completed successfully!', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

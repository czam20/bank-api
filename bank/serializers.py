import traceback
from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_number', 'amount', 'person')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'account_number': instance.account_number,
            'amount': instance.amount,
            'person': {
                'id': instance.person.id,
                'fullname': instance.person.fullname
            }
       }

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'amount', 'description', 'accounts')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # update account amount
        accountId = validated_data['accounts'].id
        account = Account.objects.filter(id = accountId).first()
        if validated_data['transaction_type'] == 'Deposit':
            account.amount += validated_data['amount']

        if validated_data['transaction_type'] == 'Withdrawal':
            account.amount -= validated_data['amount']

        Account.objects.filter(id = accountId).update(amount = account.amount)
           
        return super().create(validated_data)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'transaction_type': instance.transaction_type,
            'amount': instance.amount,
            'description': instance.description,
            'accounts': {
                'id': instance.accounts.id,
                'account_number': instance.accounts.account_number,
                'ownerId': instance.accounts.person.id,
                'ownerFullname': instance.accounts.person.fullname
            }
       }

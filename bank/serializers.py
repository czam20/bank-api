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
    accounts = AccountSerializer(read_only=True, many=True)
    accountsId = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), many=True, write_only=True, source='accounts')

    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'amount',
                  'description', 'accounts', 'accountsId')
        read_only_fields = ('id', )

    def validate(self, data):
        print(data)
        account = data['accounts'][0]

        if data['transaction_type'] == 'Withdrawal' or data['transaction_type'] == 'Transfer':
            if account.amount < data['amount']:
                raise serializers.ValidationError(
                    "You don't have enough money to carry out this transaction")

        return data

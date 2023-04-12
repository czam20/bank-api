from rest_framework import serializers
from .models import Account, Transaction
from persons.serializers import PersonSerializer
from persons.models import Person


class AccountSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    personId = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), write_only=True, source='person')

    class Meta:
        model = Account
        fields = ('id', 'account_number', 'balance',
                  'person', 'personId', 'created_at')
        read_only_fields = ('id', 'created_at')

    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'account_number': instance.account_number,
    #         'amount': float(instance.balance.to_decimal()),
    #         'person': {
    #             'id': instance.person.id,
    #             'fullname': instance.person.fullname
    #         }
    #     }


class TransactionSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(read_only=True, many=True)
    accountsId = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), many=True, write_only=True, source='accounts')

    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'amount',
                  'description', 'accounts', 'accountsId', 'date')
        read_only_fields = ('id', 'date')

    def validate(self, data):
        # print(data)
        account = data['accounts'][0]

        if data['transaction_type'] == 'Withdrawal' or data['transaction_type'] == 'Transfer':
            if float(account.balance.to_decimal()) < data['amount']:
                raise serializers.ValidationError(
                    "You don't have enough money to carry out this transaction")

        return data

from django.db import models


class Account(models.Model):
    account_number = models.PositiveIntegerField(
        unique=True, null=False, blank=False)
    amount = models.DecimalField(
        max_digits=12, decimal_places=3, null=False, blank=False)
    person = models.ForeignKey(
        'persons.Person', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.account_number)


class Transaction(models.Model):
    class TransactionTypes(models.TextChoices):
        DEPOSIT = 'Deposit', 'Deposit'
        WITHDRAWAL = 'Withdrawal', 'Withdrawal'
        TRANSFER = 'Transfer', 'Transfer'

    transaction_type = models.CharField(
        max_length=20, choices=TransactionTypes.choices, default=TransactionTypes.DEPOSIT)
    amount = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    accounts = models.ManyToManyField('Account')


class Account_Transaction(models.Model):
    class UserTypes(models.TextChoices):
        SENDER = '1', 'Sender'
        RECEIVER = '2', 'Receiver'
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    userType = models.CharField(
        max_length=1, choices=UserTypes.choices, default=UserTypes.SENDER)

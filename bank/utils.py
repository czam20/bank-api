from bson.decimal128 import Decimal128
import decimal

def modifyAccountAmount(accountAmount, transactionAmount, transactionType):
    if transactionType == 'Deposit':
        newAccountAmount = Decimal128(accountAmount.to_decimal() + decimal.Decimal(transactionAmount))
    elif transactionType == 'Withdrawal':
        newAccountAmount = Decimal128(accountAmount.to_decimal() - decimal.Decimal(transactionAmount))

    return float(newAccountAmount.to_decimal())


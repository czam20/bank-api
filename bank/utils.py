def modifyAccountAmount(accountAmount, transactionAmount, transactionType):
    if transactionType == 'Deposit':
        accountAmount += transactionAmount
    elif transactionType == 'Withdrawal':
        accountAmount -= transactionAmount

    return accountAmount

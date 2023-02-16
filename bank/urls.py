from django.urls import path
from rest_framework import routers
from .api import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()

router.register('api/accounts', AccountViewSet, 'accounts')
router.register('api/transactions', TransactionViewSet, 'transactions')


urlpatterns = [
    path('api/transactions/transfer',
         TransactionViewSet.as_view({'post': 'make_transfer'}), name='make_transfer'),
    path('api/transactions/deposit-withdrawal', TransactionViewSet.as_view(
        {'post': 'make_deposit_or_withdrawal'}), name='make_deposit_or_withdrawal')
] + router.urls

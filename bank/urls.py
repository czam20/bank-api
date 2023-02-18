from django.urls import path
from rest_framework import routers
from .api import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()

router.register('api/accounts', AccountViewSet, 'accounts')
router.register('api/transactions', TransactionViewSet, 'transactions')


urlpatterns = [
    path('api/transactions/make-transfer',
         TransactionViewSet.as_view({'post': 'make_transfer'}), name='make_transfer'),
    path('api/transactions/deposit-withdrawal', TransactionViewSet.as_view(
        {'post': 'make_deposit_or_withdrawal'}), name='make_deposit_or_withdrawal'),
    path('api/transactions/<str:type>', TransactionViewSet.as_view(
        {'get': 'get_transactions_by_type'}), name='get_transactions_by_type'),
    path('api/accounts/<int:account_id>/transactions', TransactionViewSet.as_view(
        {'get': 'get_transactions_by_account'}), name='get_transactions_by_account'),
    path('api/users/<int:user_id>/accounts', AccountViewSet.as_view(
        {'get': 'get_accounts_by_user'}), name='get_accounts_by_user'),
] + router.urls

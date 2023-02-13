from rest_framework import routers
from .api import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()

router.register('api/accounts', AccountViewSet, 'accounts')
router.register('api/transactions', TransactionViewSet, 'transactions')

urlpatterns = router.urls

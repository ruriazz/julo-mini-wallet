from django.urls import path
from apiv1.wallet.handlers import WalletHandler


app_name = 'api-v1'

urlpatterns = [
    path('init', WalletHandler.as_view({'post': 'wallet_registration'})),
    path('wallet', WalletHandler.as_view({'post': 'activate_wallet', 'get': 'wallet_balance', 'patch': 'deactivate_wallet'})),
    path('wallet/transactions', WalletHandler.as_view({'get': 'transaction_history'})),
    path('wallet/<str:action>', WalletHandler.as_view({'post': 'create_transaction'})),
]
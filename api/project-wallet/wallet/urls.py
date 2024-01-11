

from django.urls import path

from wallet.api.views import WalletAPI

urlpatterns = [
    path('balance', WalletAPI.as_view({'get': 'get_balance'})),
    path('transfer', WalletAPI.as_view({'post': 'create_transaction'})),
    path('create', WalletAPI.as_view({'post': 'create_wallet'})),
    path('payment', WalletAPI.as_view({'get': 'payment_list'})),
    path('settings', WalletAPI.as_view({'get': 'settings'}))
]

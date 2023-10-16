

from django.urls import path

<<<<<<< HEAD
from wallet.api.views import MoneroAPI

urlpatterns = [
    path('balance', MoneroAPI.as_view({'get': 'get_balance'})),
    path('transfer', MoneroAPI.as_view({'post': 'create_transaction'})),
    path('create', MoneroAPI.as_view({'post': 'create_wallet'})),
=======
from wallet.api.views import WalletAPI

urlpatterns = [
    path('balance', WalletAPI.as_view({'get': 'get_balance'})),
    path('transfer', WalletAPI.as_view({'post': 'create_transaction'})),
    path('create', WalletAPI.as_view({'post': 'create_wallet'})),
    path('payment', WalletAPI.as_view({'get': 'payment_list'})),
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
]



from django.urls import path

from wallet.api.views import MoneroAPI

urlpatterns = [
    path('balance', MoneroAPI.as_view({'get': 'get_balance'})),
    path('transfer', MoneroAPI.as_view({'post': 'create_transaction'})),
    path('create', MoneroAPI.as_view({'post': 'create_wallet'})),
]

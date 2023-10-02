

from django.urls import path

from wallet.api.views import MoneroAPI

urlpatterns = [
    path('monero/ballance', MoneroAPI.as_view({'get': 'get_balance'})),
    path('monero/transfer', MoneroAPI.as_view({'post': 'create_transaction'}))
]

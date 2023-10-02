

from django.urls import path

from wallet.api.views import MoneroAPI

urlpatterns = [
    path('monero/ballance', MoneroAPI.as_view({'get': 'get_balance'}))
]

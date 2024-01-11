


from django.urls import path

from admin_statistics.views import StatisticsAPI

urlpatterns = [
    path('all', StatisticsAPI.as_view({'get': 'get_statistic'})),
    path('create_wallet', StatisticsAPI.as_view({'post': 'create_wallet'})),
    path('exchange', StatisticsAPI.as_view({'post': 'create_exchange'}))
]

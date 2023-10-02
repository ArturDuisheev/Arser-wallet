from django.http import HttpRequest
from django.shortcuts import render
from wallet.api.serializers.monero import MoneroGetBallanceSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
# Create your views here.
from rest_framework.request import Request

from wallet.api.services.monero import MoneroService, wallet

from global_modules.exeptions import CodeDataException
from wallet.api.services.base import get_field_in_dict_or_exception


class MoneroAPI(ViewSet):

    def get_balance(self, request: Request):
        serializer = MoneroGetBallanceSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        account = MoneroService.get_account(data["account_index"])
        balance = MoneroService.get_balance(account=account)
        return Response(data={"balance": balance})



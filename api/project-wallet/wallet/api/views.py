from django.http import HttpRequest
from django.shortcuts import render
from wallet.api.monero.serializers import MoneroDataSerializer, MoneroGetBallanceSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from wallet.api.monero.services.monero import MoneroService, wallet

from global_modules.exeptions import CodeDataException
from wallet.api.enum import enum_monero as enum_monero
from wallet.api.services.base import get_field_in_dict_or_exception


class MoneroAPI(ViewSet):

    def get_balance(self, request: Request):
        serializer = MoneroGetBallanceSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            account = MoneroService.get_account(data["account_index"])
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        balance = MoneroService.get_balance(account=account)
        
        return Response(data={"balance": balance})

    def create_transaction(self, request: Request):
        serializer = MoneroDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            wallet = enum_monero.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            wallet.create_transaction(serializer=serializer)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        
        return Response()
        
    def create_wallet(self, request: Request):
        MoneroService.create_wallet()
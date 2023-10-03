from django.http import HttpRequest
from django.shortcuts import render
from tronpy import Tron
from tronpy.providers import HTTPProvider

from wallet.api.monero.serializers import NetworkSerializer, PaymentDataSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from wallet.api.monero.services.monero import MoneroService, wallet

from global_modules.exeptions import CodeDataException
from wallet.api.enum import enum_monero as enum_monero
from wallet.api.services.base import get_field_in_dict_or_exception

class MoneroAPI(ViewSet):

    def get_balance(self, request: Request):
        serializer = NetworkSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            wallet = enum_monero.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            account = wallet.get_account(request.GET)
            balance = wallet.get_balance(account)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        return Response(data={"balance": balance})

    def create_transaction(self, request: Request):
        serializer = PaymentDataSerializer(data=request.data)
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
        try:
            wallet = enum_monero.WalletEnum.get_wallet(
                request.data["network"],
            )
            address = wallet.create_wallet(request.data["label"], is_address=True)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        
        return Response(data={"wallet_id": address})

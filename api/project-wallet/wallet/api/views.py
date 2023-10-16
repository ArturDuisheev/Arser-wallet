from django.http import HttpRequest
from django.shortcuts import render
from tronpy import Tron
from tronpy.providers import HTTPProvider
from drf_yasg.utils import swagger_auto_schema
from wallet.api.monero.serializers import MoneroCreateWalletSerializer, MoneroPaymentSerializer, NetworkSerializer, PaymentDataSerializer, QuerySeralizerGetBallance
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
<<<<<<< HEAD

from wallet.api.monero.services.monero import MoneroService, wallet

=======
from wallet.models import Payment
from wallet.api.monero.services.monero import MoneroService, wallet

>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
from global_modules.exeptions import CodeDataException
from wallet.api.enum import enum_monero as enum_monero
from wallet.api.services.base import get_field_in_dict_or_exception

<<<<<<< HEAD
class MoneroAPI(ViewSet):
=======
class WalletAPI(ViewSet):
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1

    @swagger_auto_schema(tags=['wallet'], query_serializer=QuerySeralizerGetBallance)
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

    @swagger_auto_schema(tags=['wallet'], request_body=MoneroPaymentSerializer)
    def create_transaction(self, request: Request):
        serializer = NetworkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            wallet = enum_monero.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            wallet.create_transaction(data=request.data)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        
        return Response()
        
    @swagger_auto_schema(tags=['wallet'], request_body=MoneroCreateWalletSerializer)
    def create_wallet(self, request: Request):
        serializer = NetworkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            wallet = enum_monero.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            address = wallet.create_wallet(request.data)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        print(address)
        return Response(data={"wallet_info": address})
<<<<<<< HEAD
=======

    @swagger_auto_schema(tags=['wallet'])
    def payment_list(self, request: Request):
        payment_list = Payment.objects.order_by('-id').all()
        serializer = PaymentDataSerializer(payment_list, many=True)
        return Response(serializer.data, status=200)
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1

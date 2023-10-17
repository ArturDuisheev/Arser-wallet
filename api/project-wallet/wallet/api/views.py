from django.shortcuts import render
from tronpy import Tron
from drf_yasg.utils import swagger_auto_schema
from wallet.api.monero.serializers import MoneroCreateWalletSerializer, MoneroPaymentSerializer, NetworkSerializer, PaymentDataSerializer, QuerySeralizerGetBallance
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from wallet.models import Payment

from global_modules.exeptions import CodeDataException
from wallet.api.enum import enum_wallet

class WalletAPI(ViewSet):

    @swagger_auto_schema(tags=['wallet'], query_serializer=QuerySeralizerGetBallance)
    def get_balance(self, request: Request):
        serializer = NetworkSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            wallet = enum_wallet.WalletEnum.get_wallet(
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
            wallet = enum_wallet.WalletEnum.get_wallet(
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
            wallet = enum_wallet.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            address = wallet.create_wallet(request.data)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        print(address)
        return Response(data={"wallet_info": address})

    @swagger_auto_schema(tags=['wallet'])
    def payment_list(self, request: Request):
        payment_list = Payment.objects.order_by('-id').all()
        serializer = PaymentDataSerializer(payment_list, many=True)
        return Response(serializer.data, status=200)
from django.shortcuts import render
from tronpy import Tron
from drf_yasg.utils import swagger_auto_schema
from wallet.api.monero.serializers import MoneroCreateWalletSerializer, MoneroPaymentSerializer, NetworkSerializer, PaymentDataSerializer, QuerySeralizerGetBallance, WalletCreateSerializer, WalletSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from wallet.models import Payment, Wallet

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
            wallet_data = wallet.create_transaction(data=request.data)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        
        return Response(data=wallet_data)
        
    @swagger_auto_schema(tags=['wallet'], request_body=WalletCreateSerializer)
    def create_wallet(self, request: Request):
        serializer = WalletCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            wallet = enum_wallet.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            address = wallet.create_wallet(request.data)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        
        data  = {
            **serializer.validated_data,
            "address": address if type(address) == str else address["address"],

        }
        wallet_serializer = WalletSerializer(data=data)
        wallet_serializer.is_valid(raise_exception=True)
        wallet_serializer.save()
        return Response(data={**wallet_serializer.data, "wallet_info": address})

    @swagger_auto_schema(tags=['wallet'])
    def payment_list(self, request: Request):
        payment_list = Payment.objects.order_by('-uuid').all()
        serializer = PaymentDataSerializer(payment_list, many=True)
        # TODO: Заменить пересчет здесь, на пересчет в celery
        wallet_list = Wallet.objects.all()
        
        dict_wallet_list = {

        }
        
        for payment in payment_list:
            dict_wallet_list[payment.address] = payment
        for wallet in wallet_list:
            wallet_engine = enum_wallet.WalletEnum.get_wallet(
                "XMR" if wallet.network == "MONERO" else wallet.network,
            )
            account = wallet_engine.get_account({
                "address": wallet.address,
                "account_index": 1
            })
            balance = wallet_engine.get_balance(account)
            print(balance)
        return Response(serializer.data, status=200)
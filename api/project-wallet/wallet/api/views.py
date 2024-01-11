import time

import requests
from django.shortcuts import render
from tronpy import Tron
from drf_yasg.utils import swagger_auto_schema

from wallet.api.monero.MoneroWallet import MoneroWallet
from wallet.api.monero.serializers import MoneroCreateWalletSerializer, MoneroPaymentSerializer, NetworkSerializer, PaymentDataSerializer, QuerySeralizerGetBallance, WalletCreateSerializer, WalletSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from wallet.api.monero.services.monero import MoneroService
from wallet.api.ton.TonWallet import TonWallet
from wallet.api.tron.TronWallet import TronWallet
from wallet.choices import NetWorkChoice, CurrencyChoice
from wallet.models import Payment, Wallet, WalletSettings
from wallet.api.btc import BtcWallet
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
            wallet_data = wallet.create_transaction(data=request.data.copy())
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        return Response(data=wallet_data)
        
    @swagger_auto_schema(tags=['wallet'], request_body=WalletCreateSerializer)
    def create_wallet(self, request: Request):
        serializer = WalletCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(123)
        try:
            wallet = enum_wallet.WalletEnum.get_wallet(
                serializer.data["network"],
            )
            address = wallet.create_wallet(request.data)
        except CodeDataException as e:
            return Response(data=e.error_data, status=e.status)
        print(address)
        data = {
            **serializer.validated_data,
            "address": address if type(address) == str else address["address"],

        }
        if serializer.data["network"] == NetWorkChoice.TON:
            data['mnemonics'] = ",".join(address["mnemonics"])
        if not serializer.data["network"] == NetWorkChoice.TRON:
            wallet_serializer = WalletSerializer(data=data)
            wallet_serializer.is_valid(raise_exception=True)
            wallet_serializer.save()
        return Response(data={**data, "wallet_info": address})

    @swagger_auto_schema(tags=['wallet'])
    def payment_list(self, request: Request):
        # TODO: Заменить пересчет здесь, на пересчет в celery
        wallet_list = Wallet.objects.all()

        for wallet in wallet_list:
            if wallet.network == NetWorkChoice.TON:
                init_ton_wallet(wallet)
            if wallet.network == NetWorkChoice.TRON:
                init_tron_usdt_wallet(wallet)
            if wallet.network == NetWorkChoice.XMR:
                init_xmr_wallet(wallet)
            if wallet.network == NetWorkChoice.BTC:
                init_btc_wallet(wallet)
        payment_list = Payment.objects.all()
        serializer = PaymentDataSerializer(payment_list, many=True)
        # dict_wallet_list = {
        #
        # }
        #
        # for payment in payment_list:
        #     dict_wallet_list[payment.address] = payment
        # for wallet in wallet_list:
        #     wallet_engine = enum_wallet.WalletEnum.get_wallet(
        #         "XMR" if wallet.network == "MONERO" else wallet.network,
        #     )
        #     account = wallet_engine.get_account({
        #         "address": wallet.address,
        #         "account_index": 1
        #     })
        #     balance = wallet_engine.get_balance(account)
        #     print(balance)
        return Response(serializer.data, status=200)


    def settings(self, request):
        try:
            settings = WalletSettings.objects.last()
            return {
                "count_commission": settings.count_commission
            }
        except:
            return Response(status=404)

def init_btc_wallet(wallet: Wallet):
    try:
        account = BtcWallet().get_account(wallet.address)
        balance = BtcWallet().get_balance(account)
        if wallet.balance == 0 and balance != 0:
            # если баланс был пополнен, то начинаем его активацию
            ser = PaymentDataSerializer(data={
                "network": wallet.network,
                "amount": balance,
                "currency": CurrencyChoice.XMR,
                "order_id": 1,
                "address": wallet.address,
                "url_callback": "1"
            })
            ser.is_valid(raise_exception=True)
            ser.save()
            wallet.balance = balance
            wallet.save()
        elif wallet.balance < balance:
            ser = PaymentDataSerializer(data={
                "network": wallet.network,
                "amount": balance - wallet.balance,
                "currency": CurrencyChoice.XMR,
                "order_id": 1,
                "address": wallet.address,
                "url_callback": "1"
            })
            ser.is_valid(raise_exception=True)
            ser.save()
            wallet.balance = balance
            wallet.save()
        else:
            wallet.balance = balance
            wallet.save()
    except:
        ...


def init_xmr_wallet(wallet: Wallet):
    try:
        account = MoneroService().get_account(address=wallet.address)
        balance_xmr = MoneroWallet().get_balance(account=account)['balance']

        if wallet.balance == 0 and balance_xmr != 0:
            # если баланс был пополнен, то начинаем его активацию
            ser = PaymentDataSerializer(data={
                "network": wallet.network,
                "amount": balance_xmr,
                "currency": CurrencyChoice.XMR,
                "order_id": 1,
                "address": wallet.address,
                "url_callback": "1"
            })
            ser.is_valid(raise_exception=True)
            ser.save()
            wallet.balance = balance_xmr
            wallet.save()
        elif wallet.balance < balance_xmr:
            ser = PaymentDataSerializer(data={
                "network": wallet.network,
                "amount": balance_xmr - wallet.balance,
                "currency": CurrencyChoice.XMR,
                "order_id": 1,
                "address": wallet.address,
                "url_callback": "1"
            })
            ser.is_valid(raise_exception=True)
            ser.save()
            wallet.balance = balance_xmr
            wallet.save()
        else:
            wallet.balance = balance_xmr
            wallet.save()
    except:
        ...


def init_tron_usdt_wallet(wallet: Wallet):
    balance_tron = float(TronWallet().get_balance(wallet.address)['balance'])
    print(wallet.address)
    if wallet.balance == 0 and balance_tron != 0:
        # если баланс был пополнен, то начинаем его активацию
        ser = PaymentDataSerializer(data={
            "network": wallet.network,
            "amount": balance_tron,
            "currency": CurrencyChoice.USDT,
            "order_id": 1,
            "address": wallet.address,
            "url_callback": "1"
        })
        ser.is_valid(raise_exception=True)
        ser.save()
        wallet.balance = balance_tron
        wallet.save()
    elif wallet.balance < balance_tron:
        ser = PaymentDataSerializer(data={
            "network": wallet.network,
            "amount": balance_tron - wallet.balance,
            "currency": CurrencyChoice.USDT,
            "order_id": 1,
            "address": wallet.address,
            "url_callback": "1"
        })
        ser.is_valid(raise_exception=True)
        ser.save()
        wallet.balance = balance_tron
        wallet.save()
    else:
        wallet.balance = balance_tron
        wallet.save()


def get_ton_balance(address: str):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://testnet.toncenter.com/api/v2/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'address': address,
    }

    data = requests.get(f"https://testnet.toncenter.com/api/v2/getAddressBalance",
                            params=params, headers=headers).json()

    print(data, address)
    if data['ok'] == False:
        if data['error'] == "Rate limit exceeded: 1 per 1 second":
            time.sleep(1)
            return get_ton_balance(address)
    if int(data['result']) == 0:
        return 0
    return int(data['result']) / 1_000_000_000



def init_ton_wallet(wallet: Wallet):
    balance_ton = get_ton_balance(wallet.address)
    if wallet.balance == 0 and balance_ton != 0:
        # если баланс был пополнен, то начинаем его активацию
        try:
            wallet_ser = TonWallet()
            wallet_ser.create_wallet({
                "activate": True,
                "mnemonics": wallet.mnemonics.split(",")
            })
        except:
            ...
        finally:

            ser = PaymentDataSerializer(data={
                "network": wallet.network,
                "amount": balance_ton,
                "currency": CurrencyChoice.TON,
                "order_id": 1,
                "address": wallet.address,
                "url_callback": "1"
            })
            ser.is_valid(raise_exception=True)
            ser.save()
            wallet.balance = balance_ton
            wallet.save()
    elif wallet.balance < balance_ton:
        ser = PaymentDataSerializer(data={
            "network": wallet.network,
            "amount": balance_ton - wallet.balance,
            "currency": CurrencyChoice.TON,
            "order_id": 1,
            "address": wallet.address,
            "url_callback": "1"
        })
        ser.is_valid(raise_exception=True)
        ser.save()
        wallet.balance = balance_ton
        wallet.save()
    else:
        wallet.balance = balance_ton
        wallet.save()


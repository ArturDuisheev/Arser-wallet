import asyncio

import aiohttp
import requests
from asgiref.sync import sync_to_async, async_to_sync
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from admin_statistics.serializer import ExchangeSerializer
from wallet.api.btc.convert import BtcConverter
from wallet.api.enum.enum_wallet import WalletEnum
from wallet.api.monero.services.convert import MoneroConverter
from wallet.api.ton.convert import TonConverter
from wallet.api.tron.TronWallet import TronWallet
from wallet.api.tron.services.convert import TronUsdtConverter
from wallet.choices import NetWorkChoice
from wallet.models import Payment, Wallet, Exchange


# Create your views here.

async def get_converter(network):
    if network == NetWorkChoice.TRON:
        wallet = TronUsdtConverter()
    elif network == NetWorkChoice.TON:
        wallet = TonConverter()
    elif network == NetWorkChoice.BTC:
        wallet = BtcConverter()
    elif network == NetWorkChoice.XMR:
        wallet = MoneroConverter()
    return wallet


@sync_to_async
def get_all_exchange():
    return list(Exchange.objects.all())


async def get_(params):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=f"https://min-api.cryptocompare.com/data/pricemulti", params=params
        )
        data_response = await response.json()
        print(data_response)
        await asyncio.sleep(1.2)
        if data_response.get('status'):
            await asyncio.sleep(30)
            return await get_(params)
        return data_response


async def get_payment_amount_total():
    payment_list = await get_all_exchange()
    data = {
        'usdt': 0.0,
        'rub': 0
    }
    await sync_to_async(print)(payment_list)
    data_cache = {
        "spot": {

        },
        "base": {

        }
    }
    for payment in payment_list:
        payment_converter = await get_converter(payment.network)
        async with aiohttp.ClientSession() as session:
            if not data_cache['spot'].get(f"{payment_converter.spot}-USDT"):
                response = await session.get(
                    url=f"https://api.coinbase.com/v2/prices/{payment_converter.spot}-USDT/spot"
                )
                data_response = await response.json()
                data_cache['spot'][f"{payment_converter.spot}-USDT"] = data_response['data']['amount']
                print(data_response['data']['amount'], payment.amount)
            else:
                data_response = {
                    'data': {
                        'amount': data_cache['spot'].get(f"{payment_converter.spot}-USDT")
                    }
                }
            params = {
                "fsyms": payment_converter.spot,
                "tsyms": 'rub'
            }
            data['usdt'] += float(data_response['data']['amount']) * float(payment.amount)
            print(not data_cache['spot'].get(f"{payment_converter.spot}-RUB"), f"{payment_converter.spot}-RUB")
            if not data_cache['spot'].get(f"{payment_converter.spot}-RUB"):
                data_response = await get_(params)
                data_cache['spot'][f"{payment_converter.spot}-RUB"] = data_response[payment_converter.spot]['RUB']
            else:
                data_response = {
                    payment_converter.spot: {
                        "RUB": data_cache['spot'].get(f"{payment_converter.spot}-RUB")
                    }
                }
            data['rub'] += float(data_response[payment_converter.spot]['RUB']) * float(payment.amount)

    return data


class StatisticsAPI(ViewSet):

    def get_statistic(self, request):

        data = {
            'total_count': Payment.objects.count(),
            'total_summ': async_to_sync(get_payment_amount_total)()
        }

        return Response(data)

    def create_wallet(self, request):
        wallet = WalletEnum.get_wallet(request.data['n'])
        if request.data.get('n') == "TRON":
            wallet_address = wallet.create_wallet({})
            wallet_admin = Wallet.objects.get(address=wallet_address)
            wallet_admin.is_admin = True
            wallet_admin.save()
        else:
            wallet_address = wallet.create_wallet({})
            Wallet.objects.create(
                network=NetWorkChoice.TRON,
                currency=request.data.get('n'),
                order_id=1,
                address=wallet_address if type(wallet_address) == str else wallet_address["address"],
                url_callback='1',
                is_admin=True

            )
        return redirect("/admin")

    def create_exchange(self, request):
        serializer = ExchangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)

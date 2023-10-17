
from bitcoin.wallet import CBitcoinAddress
from bitcoin.rpc import RawProxy
from django.conf import settings


def get_client(wallet_name: str):
    return RawProxy(f'{settings.BTC_HTTP_URL}/wallet/{wallet_name}')
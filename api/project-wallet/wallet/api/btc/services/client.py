
from bitcoin.wallet import CBitcoinAddress
from bitcoin.rpc import RawProxy


def get_client(wallet_name: str):
    return RawProxy(f'http://username:password@91.107.125.191:18443/wallet/{wallet_name}')
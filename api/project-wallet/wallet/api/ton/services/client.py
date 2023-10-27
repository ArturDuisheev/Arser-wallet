import requests
from pathlib import Path
import asyncio
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from pytonlib import TonlibClient
from wallet.api.ton.services.config import config_client
from django.conf import settings
from TonTools import TonCenterClient

def get_client() -> TonCenterClient:
    config_cli = config_client


    keystore_dir = '/tmp/ton_keystore/'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)
    client_ton = TonCenterClient(testnet=True)
    return client_ton

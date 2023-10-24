import requests
from pathlib import Path
import asyncio
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from pytonlib import TonlibClient
from wallet.api.ton.services.config import config_client
from django.conf import settings


async def get_client() -> TonlibClient:
    config_cli = config_client


    keystore_dir = '/tmp/ton_keystore/'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)
    client_ton = TonlibClient(ls_index=1, config=config_cli, keystore=keystore_dir)
    await client_ton.init()
    return client_ton

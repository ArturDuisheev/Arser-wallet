import requests
from pathlib import Path
import asyncio
from pytonlib import TonlibClient




url = 'https://ton.org/testnet-global.config.json'

config = requests.get(url).json()

keystore_dir = '/tmp/ton_keystore/'
Path(keystore_dir).mkdir(parents=True, exist_ok=True)

client_ton = TonlibClient(ls_index=14, config=config, keystore=keystore_dir, tonlib_timeout=15)

asyncio.get_event_loop().run_until_complete(client_ton.init())
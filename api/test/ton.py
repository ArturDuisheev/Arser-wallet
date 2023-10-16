import asyncio
from config import testnet
from wallet_creation import wallet
from tonsdk.utils import to_nano
import requests
from pathlib import Path
import asyncio
from pytonlib import TonlibClient


async def get_seqno(client: TonlibClient, address: str):
    return await client.raw_run_method(method='seqno', stack_data=[], address=address)

async def main():
    
    query = wallet.create_init_external_message()
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore/'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client_ton = TonlibClient(ls_index=10, config=config, keystore=keystore_dir, tonlib_timeout=15)

    await client_ton.init()
    deploy_message = query["message"].to_boc(False)
    wallet_adress = wallet.address.to_string(True, True, True, True)


    transfer_query = wallet.create_transfer_message(to_addr="EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N", amount=to_nano(0.01, 'ton'), seqno=1)

    transfer_message = transfer_query["message"].to_boc(False)

    await client_ton.raw_send_message(transfer_message)



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
import codecs
import json
from hexbytes import HexBytes
from global_modules.exeptions import CodeDataException

from django.conf import settings
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import to_hex_address
from tronpy.keys import PrivateKey
from tronpy.contract import Contract
from tronpy.tron import TransactionBuilder, Transaction
from solc.main import get_solc_version
from .abi import abi
from .bytecode import bytecode

client = Tron(HTTPProvider(settings.TRON_HTTP_URL)) 


class UsdtTronService:

    @classmethod
    def get_balance(cls, account: dict) -> float:
        
        return account.get('balance')
    
    @classmethod
    def get_account(cls, address: str) -> dict:
        try:
            return client.get_account(address)
        except IndexError:
            raise CodeDataException("Неверный адресс аккаунта")

    
    @classmethod
    def create_wallet(cls, **kwargs) -> str:
        priv_key = PrivateKey(bytes.fromhex(settings.PRIVATE_KEYS_FROM_ADDRESS_TRON))
        contract = Contract(client=client, origin_address=priv_key.public_key.to_base58check_address(),
                             owner_address=priv_key.public_key.to_base58check_address(),
                            abi=abi,bytecode = bytecode

                            )
        deployed_contract = contract.deploy()
        txn = (
                    deployed_contract
                    .fee_limit(20_000_000)
                    .build()
                    .sign(priv_key)
                )
        result = txn.broadcast().wait()
        print(result)
        return result['contract_address']
    @classmethod
    def create_transaction(cls, from_address: str, to_address: str, amount: int, priv_key: PrivateKey):
        contract = client.get_contract(settings.TRON_USDT_CONTRACT)
        contract.abi = abi
        priv_key = PrivateKey(bytes.fromhex(settings.PRIVATE_KEYS_FROM_ADDRESS_TRON))
        amount_in_wei = int(amount * 10 ** 6)
        tx = contract.functions.transfer(to_address, amount_in_wei).with_owner(priv_key.public_key.to_base58check_address())
        tx = tx.build()
        signed_txn = tx.sign(priv_key)
        data = signed_txn.broadcast()['txid']
        signed_txn.broadcast().wait()
        return data

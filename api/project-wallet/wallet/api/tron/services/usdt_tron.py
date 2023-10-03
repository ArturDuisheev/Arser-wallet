
from global_modules.exeptions import CodeDataException
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey

client = Tron(HTTPProvider("http://217.28.220.195:9090")) 


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
    def create_transaction(cls, from_address: str, to_address: str):
        client.trx.transfer(from_=from_address, to_=to_address, )
    
    @classmethod
    def create_wallet(cls, label: str):
        address = client.generate_address()
        print(bytes.fromhex("80372a65283f3134aef6e9dc39e72d1800ebb91077b7e80551f88d3dd4f037d2"), 21)
        priv_key = PrivateKey(bytes.fromhex("80372a65283f3134aef6e9dc39e72d1800ebb91077b7e80551f88d3dd4f037d2"))
        print(priv_key.public_key)
        trans_build = client.trx.transfer(from_=priv_key.public_key, to=address["base58check_address"], amount=1)
        transac = trans_build.build()
        transac.sign(priv_key)
        return address
    
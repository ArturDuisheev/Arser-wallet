from global_modules.exeptions import CodeDataException

from django.conf import settings
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
    def create_wallet(cls, **kwargs) -> str:
        address = client.generate_address()
        priv_key = PrivateKey(bytes.fromhex(settings.PRIVATE_KEYS_FROM_ADDRESS_TRON))
        cls.create_transaction(from_address=settings.FROM_ADDRESS_TRON, to_address=address["hex_address"], amount=1,
                                      priv_key=priv_key)
        client.to_canonical_address(address["hex_address"])
        return client.to_canonical_address(address["hex_address"])
    
    @classmethod
    def create_transaction(cls, from_address: str, to_address: str, amount: int, priv_key: PrivateKey):
        tran = client.trx.transfer(from_=from_address, to=to_address, amount=amount).build().sign(priv_key)      
        tran.txid
        tran.broadcast().wait()
        return tran

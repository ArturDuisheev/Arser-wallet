from django.conf import settings

from monero.backends.jsonrpc import JSONRPCWallet
from monero.wallet import Wallet
from global_modules.exeptions import CodeDataException

wallet = Wallet(JSONRPCWallet(host=settings.MONERO_HOST, port=settings.MONERO_PORT,
                               user=settings.MONERO_USER, password=settings.MONERO_PASSWORD))


class MoneroService:

    @classmethod
    def get_balance(cls, account) -> float:
        return account.balance()
    
    @classmethod
    def get_account(cls, index: int):
        try:
            
            return wallet.accounts[index]
        except IndexError:
            raise CodeDataException("Неверный индекс аккаунта")
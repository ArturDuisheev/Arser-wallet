from tronpy import Tron
from wallet.models import Payment
from django.conf import settings
from tronpy.providers import HTTPProvider
from monero.backends.jsonrpc import JSONRPCWallet
from monero.wallet import Wallet
from global_modules.exeptions import CodeDataException
from monero.account import Account



wallet = Wallet(JSONRPCWallet(host=settings.MONERO_HOST, port=settings.MONERO_PORT,
                               user=settings.MONERO_USER, password=settings.MONERO_PASSWORD))


class MoneroService:

    @classmethod
    def get_balance(cls, account: Account) -> float:
        
        return {
            "balance": account.balance(),
            "unlocked": account.balance(unlocked=True)
                }
    
    @classmethod
    def get_account(cls, index: int, address=None) -> Account:
        try:
            if address is None:
                return wallet.accounts[index]
            else:
                for account in wallet.accounts:
                    account: Account
                    print(1)
                    for address_ in account.addresses():
                        if address_ == address:
                            return account
                else:
                    raise CodeDataException("Неверный адресс аккаунта")

        except IndexError:
            raise CodeDataException("Неверный индекс аккаунта")

    @classmethod
    def create_transaction(cls, amount: float):
        return wallet.transfer(
            amount=amount,
            address=cls.get_account(0).address
        )
    
    @classmethod
    def create_wallet(cls, label: str, account: Account) -> Account:
        return account.new_address(label=label)

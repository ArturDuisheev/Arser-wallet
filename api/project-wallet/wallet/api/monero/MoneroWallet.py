
from wallet.models import Payment
from wallet.api.monero.services.monero import MoneroService


class MoneroWallet:
    """ Класс для работы с Monero"""

    def __init__(self, account_index=0) -> None:
        
        self.account = MoneroService.get_account(account_index)

    def get_balance(self, account=None) -> float:
        if account is None:
            return MoneroService.get_balance(account=self.account)
        else:
            return MoneroService.get_balance(account=account)
    def create_transaction(self, amount: float, address: str):
        self.account.transfer(amount, address)


    def create_payment_model(**kwargs):
        return Payment.objects.create(**kwargs)
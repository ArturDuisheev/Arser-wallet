
import decimal
from wallet.api.monero.serializers import MoneroDataSerializer
from wallet.models import Payment
from wallet.api.monero.services.monero import MoneroService
from wallet.api.monero.services.convert import MoneroConverter

class MoneroWallet:
    """ Класс для работы с Monero"""


    converter = MoneroConverter()


    def __init__(self, account_index=0) -> None:
        
        self.account = MoneroService.get_account(account_index)

    def get_balance(self, account=None) -> float:
        if account is None:
            return MoneroService.get_balance(account=self.account)
        else:
            return MoneroService.get_balance(account=account)
    
    def _get_atomic_amount(self, amount: str, currency: str):
        return self.converter(amount=amount, currency=currency)


    def create_transaction(self, serializer: MoneroDataSerializer):
        amount = self._get_atomic_amount(serializer.data["amount"], serializer.data["currency"])
        transfer = self.account.transfer(amount, serializer.data["address"])
        print(transfer)
        return self._create_payment_model(serializer)
        print(amount)

    
    def _create_payment_model(serializer: MoneroDataSerializer) -> Payment:
        return serializer.save()
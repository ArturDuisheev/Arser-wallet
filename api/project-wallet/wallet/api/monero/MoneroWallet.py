
from global_modules.exeptions import CodeDataException

from wallet.api.services.base import get_field_in_dict_or_exception
from wallet.api.monero.serializers import PaymentDataSerializer
from wallet.models import Payment
from wallet.api.monero.services.monero import MoneroService
from wallet.api.monero.services.convert import MoneroConverter

from tronpy.exceptions import AddressNotFound

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
    
    def get_account(self, data: dict):
        account_index = get_field_in_dict_or_exception(data, "account_index", "Вы не указали account_index")
        try:
            return MoneroService.get_account(int(account_index))
        except AddressNotFound:
            raise CodeDataException("Неверный адресс аккаунта")


    def _get_atomic_amount(self, amount: str, currency: str):
        return self.converter(amount=amount, currency=currency)


    def create_transaction(self, serializer: PaymentDataSerializer):
        amount = self._get_atomic_amount(serializer.data["amount"], serializer.data["currency"])
        transfer = self.account.transfer(amount, serializer.data["address"])
        print(transfer)
        return self._create_payment_model(serializer)

    
    def _create_payment_model(serializer: PaymentDataSerializer) -> Payment:
        return serializer.save()
    

    def create_wallet(self, data: dict) -> str:
        label = get_field_in_dict_or_exception(data, "label", "Вы не указали label")
        return str(MoneroService.create_wallet(label=label).index)

import decimal

from wallet.api.services.base import get_field_in_dict_or_exception

from wallet.api.tron.services.usdt_tron import UsdtTronService
from wallet.api.monero.serializers import PaymentDataSerializer
from wallet.models import Payment

class TronWallet:
    """ Класс для работы с Tron"""


    converter = None


    def get_balance(self, account=None) -> float:
        return UsdtTronService.get_balance(account)
    
    def _get_atomic_amount(self, amount: str, currency: str):
        return self.converter(amount=amount, currency=currency)


    def create_transaction(self, serializer: PaymentDataSerializer):
        amount = self._get_atomic_amount(serializer.data["amount"], serializer.data["currency"])
        transfer = self.account.transfer(amount, serializer.data["address"])
        print(transfer)
        return self._create_payment_model(serializer)

    
    def _create_payment_model(serializer: PaymentDataSerializer) -> Payment:
        return serializer.save()
    

    def create_wallet(self, data: dict):
        
        return UsdtTronService.create_wallet(data=data)
    
    def get_account(self, data: dict):
        address = get_field_in_dict_or_exception(data, "address", "Вы не указали address")
        return UsdtTronService.get_account(address=address)
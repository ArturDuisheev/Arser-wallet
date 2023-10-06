
from global_modules.exeptions import CodeDataException

from wallet.api.services.base import get_field_in_dict_or_exception
from wallet.api.monero.serializers import MoneroPaymentSerializer, PaymentDataSerializer
from wallet.models import Payment
from wallet.api.monero.services.monero import MoneroService, wallet as w
from wallet.api.monero.services.convert import MoneroConverter
from monero.exceptions import NotEnoughUnlockedMoney, NotEnoughMoney


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
        return MoneroService.get_account(int(account_index))


    def _get_atomic_amount(self, amount: str, currency: str):
        return self.converter(amount=amount, currency=currency)


    def create_transaction(self, data: dict):

        serializer = MoneroPaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get("from_", None):
            self.account = self.get_account({
                "account_index": serializer.validated_data["from_"],
            })
        amount = self._get_atomic_amount(serializer.validated_data["amount"], serializer.validated_data["currency"])
        print(amount)
        try:
            transfer = self.account.transfer(amount=amount, address=serializer.validated_data["address"])
        except NotEnoughUnlockedMoney:
            raise CodeDataException("Недостаточно разблокированных средств")
        except NotEnoughMoney:
            raise CodeDataException("NotEnoughMoney")
        print(transfer[0], transfer[0].__dict__)
        return self._create_payment_model(serializer)

    
    def _create_payment_model(self, serializer: MoneroPaymentSerializer) -> dict:
        serializer.save()
        return serializer.data
    
    def create_wallet(self, data: dict) -> str:
        label = get_field_in_dict_or_exception(data, "label", "Вы не указали label")
        wallet_new = MoneroService.create_wallet(label=label)
        return dict(id=wallet_new.index, address=str(wallet_new.address()))
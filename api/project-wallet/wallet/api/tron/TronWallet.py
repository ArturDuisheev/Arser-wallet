from wallet.api.tron.services.convert import TronUsdtConverter

from django.conf import settings

from wallet.api.services.base import get_field_in_dict_or_exception

from wallet.api.tron.services.usdt_tron import UsdtTronService
from wallet.api.monero.serializers import PaymentDataSerializer
from wallet.models import Payment

from tronpy.keys import PrivateKey


class TronWallet:
    """ Класс для работы с Tron"""

    converter = TronUsdtConverter()

    def get_balance(self, account=None) -> dict:
        balance = UsdtTronService.get_balance(account)
        data = {
            "balance": balance,
            "unlocked": balance
        }
        return data

    def _get_atomic_amount(self, amount: str, currency: str):
        return self.converter(amount=amount, currency=currency)

    def create_transaction(self, data: dict):
        serializer = PaymentDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        transfer = UsdtTronService.create_transaction(from_address=settings.FROM_ADDRESS_TRON,
                                                      to_address=serializer.validated_data["address"], amount=amount)
        print(transfer)
        obj = self._create_payment_model(serializer)
        return {**PaymentDataSerializer(obj).data, "txid": transfer}

    def _create_payment_model(self, serializer: PaymentDataSerializer) -> Payment:
        return serializer.save()

    def create_wallet(self, data: dict):
        return UsdtTronService.create_wallet(data=data)

    def get_account(self, data: dict):
        address = get_field_in_dict_or_exception(data, "address", "Вы не указали address")
        return UsdtTronService.get_account(address=address)

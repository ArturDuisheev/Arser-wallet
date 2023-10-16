
import asyncio
from wallet.api.btc.convert import BtcConverter
from tonsdk.contract.wallet import Wallets

from wallet.api.monero.serializers import PaymentDataSerializer

from wallet.api.btc.services.btc import BtcService

from django.conf import settings

from wallet.api.services.base import get_field_in_dict_or_exception


class BtcWallet:

    
    def get_account(self, data: dict):
        address = get_field_in_dict_or_exception(data, "address", "Вы не указали address")
        return address

    conterter = BtcConverter()

    def create_wallet(self, data: dict):
        return BtcService.create_wallet(data)
    
    def create_transaction(self, data: dict):
        serializer = PaymentDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        amount = self.conterter(amount=data.get("amount"), currency=data.get("currency"))
        BtcService.create_transaction(amount=round(amount, 3), address=self.get_account(data))
        return self._create_payment_model(serializer)
    
    def get_balance(self, account):
        return BtcService.get_balance(account=account)

    def _create_payment_model(self, serializer: PaymentDataSerializer) -> dict:
        serializer.save()
        return serializer.data
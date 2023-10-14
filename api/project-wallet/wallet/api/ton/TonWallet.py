
import asyncio
from tonsdk.contract.wallet import Wallets

from wallet.api.monero.serializers import PaymentDataSerializer

from wallet.api.ton.convert import TonConverter
from wallet.api.ton.services.ton import TonService

from django.conf import settings

from wallet.api.services.base import get_field_in_dict_or_exception


class TonWallet:

    conterter = TonConverter()


    def __init__(self) -> None:
        _, _, _,self.account = TonService.get_account({
            'mnemonics':settings.TON_MNEMONICS.split(','),
            })
        print(self.account, 12321312)
    
    def get_account(self, data: dict):
        address = get_field_in_dict_or_exception(data, "address", "Вы не указали address")
        return address


    def create_wallet(self, data: dict):
        return asyncio.run(TonService.create_wallet(data=data))
    
    def create_transaction(self, data: dict):
        serializer = PaymentDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        amount = self.conterter(amount=data.get("amount"), currency=data.get("currency"))
        if data.get("mnemonics", False):
            print(123)
            data =  asyncio.run(TonService.create_transaction(amount=amount,
                                                             address=data.get("address"),
                                                             wallet=TonService.get_account(data=data)[3]))
        else:
            data =  asyncio.run(TonService.create_transaction(amount=amount,
                                                              address=data.get("address"),
                                                              wallet=self.account
                                                                  ))
        self._create_payment_model(serializer)
        return data
    
    def get_balance(self, account=None):
        return asyncio.run(TonService.get_balance(account=account))

    def _create_payment_model(self, serializer: PaymentDataSerializer) -> dict:
        serializer.save()
        return serializer.data
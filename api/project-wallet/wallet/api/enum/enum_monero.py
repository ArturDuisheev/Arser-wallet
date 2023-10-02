from enum import Enum

from rest_framework import status
from wallet.api.monero.MoneroWallet import MoneroWallet
from global_modules.exeptions import CodeDataException


class WalletEnum(Enum):
    monero = MoneroWallet

    @classmethod
    def get_wallet(cls, wallet_type: str):
        try:
            return cls[wallet_type]
        except KeyError:
            raise CodeDataException(status=status.HTTP_400_BAD_REQUEST, error=f"Wallet type {wallet_type} is not "
                                                                              f"supported.")




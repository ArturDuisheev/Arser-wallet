from enum import Enum

<<<<<<< HEAD
=======
from wallet.api.btc.BtcWallet import BtcWallet

>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
from wallet.api.ton.TonWallet import TonWallet
from wallet.api.tron.TronWallet import TronWallet

from rest_framework import status
from wallet.api.monero.MoneroWallet import MoneroWallet
from global_modules.exeptions import CodeDataException


class WalletEnum(Enum):
    MONERO = MoneroWallet
    TRON = TronWallet
    TON = TonWallet
<<<<<<< HEAD
=======
    BTC = BtcWallet
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1

    @classmethod
    def get_wallet(cls, wallet_type: str):
        try:
            return cls[wallet_type].value()
        except KeyError:
            raise CodeDataException(status=status.HTTP_400_BAD_REQUEST, error=f"Wallet type {wallet_type} is not "
                                                                              f"supported.")




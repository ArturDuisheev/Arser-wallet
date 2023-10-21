from enum import Enum

from wallet.api.btc.BtcWallet import BtcWallet

from wallet.api.ton.TonWallet import TonWallet
from wallet.api.tron.TronWallet import TronWallet

from rest_framework import status
from wallet.api.monero.MoneroWallet import MoneroWallet
from global_modules.exeptions import CodeDataException


class WalletEnum(Enum):
    XMR = MoneroWallet
    TRON = TronWallet
    TON = TonWallet
    BTC = BtcWallet

    @classmethod
    def get_wallet(cls, wallet_type: str):
        try:
            return cls[wallet_type].value()
        except KeyError:
            raise CodeDataException(status=status.HTTP_400_BAD_REQUEST, error=f"Wallet type {wallet_type} is not "
                                                                              f"supported.")




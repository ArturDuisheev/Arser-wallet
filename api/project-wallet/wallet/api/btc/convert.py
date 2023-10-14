import decimal
from typing import Any
from wallet.api.services.base import Converter
from tonsdk.utils import to_nano



class BtcConverter(Converter):
    
    ids = "bitcoin"

    atomic_utils = 1_000_000_000_000

    def __call__(self, amount: str, currency: str) -> float:
        self.vs_currencies = currency.lower()
        curs = self.convert_to_xmr()
        print(curs)
        return amount / curs
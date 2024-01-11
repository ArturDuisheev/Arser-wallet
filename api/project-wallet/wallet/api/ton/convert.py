

import decimal
from typing import Any
from wallet.api.services.base import Converter
from tonsdk.utils import to_nano



class TonConverter(Converter):

    spot = 'TON'
    
    ids = "the-open-network"

    atomic_utils = 1_000_000_000_000

    def __call__(self, amount: str, currency: str) -> float:
        self.vs_currencies = currency.lower()
        curs = self.convert_to_xmr()
        print(curs)
        return to_nano(float(amount) / curs, 'ton')
        
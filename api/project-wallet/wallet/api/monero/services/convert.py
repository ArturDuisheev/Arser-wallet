

import decimal
from typing import Any
from wallet.api.services.base import Converter


class MoneroConverter(Converter):
    
    ids = "monero"

    atomic_utils = 1_000_000_000_000

    def __call__(self, amount: str, currency: str) -> float:
        self.vs_currencies = currency.lower()
        curs = self.convert_to_xmr(amount=amount)
        return decimal.Decimal(amount) / decimal.Decimal(curs)
        
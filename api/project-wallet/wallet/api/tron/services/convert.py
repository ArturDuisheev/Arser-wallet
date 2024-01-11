import decimal
from wallet.api.services.base import Converter


class TronUsdtConverter(Converter):

    spot = 'USDT'

    ids = "tether"

    atomic_utils = 1_000_000_000_000

    def __call__(self, amount: str, currency: str) -> float:
        self.vs_currencies = currency.lower()
        curs = self.convert_to_xmr()
        return decimal.Decimal(amount) / decimal.Decimal(curs)
        
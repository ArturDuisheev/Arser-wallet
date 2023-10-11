
import asyncio
from wallet.api.ton.services.ton import TonService


class TonWallet:

    def create_wallet(self, data: dict):
        return asyncio.run(TonService.create_wallet(data=data))
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from django.conf import settings
import asyncio
from wallet.api.ton.services.client import get_client

from pytonlib.tonlibjson import ExternalMessageNotAccepted



class TonService:
    """ Класс для работы с TON"""

    def get_balance(self, account=None) -> dict:
        pass

    @classmethod
    async def create_wallet(self, data: dict):
        if not data.get("activate", False):
            mnemonics, _, _, wallet = Wallets.create(version=WalletVersionEnum.v3r2, workchain=0)
            return {
                "address": wallet.address.to_string(*[True * 4 if settings else True * 3]),
                "mnemonics": mnemonics
            }
        else:
            print('1234')
            client = await get_client()
            print('client')
            _, _, _, wallet = Wallets.from_mnemonics(mnemonics=data.get("mnemonics"),version=WalletVersionEnum.v3r2, workchain=0)
            query = wallet.create_init_external_message()
            deploy_message = query["message"].to_boc(False)
            try:
                await client.raw_send_message(deploy_message)
                return {
                    "message": "success"
                }
            except ExternalMessageNotAccepted:
                
                data_response = {
                    "message": "Wallet balance is null, please to replenish your wallet",
                    
                }
                if settings.DEBUG:
                    data_response["additional"] = "Данное сообщение вы видите т.к приложение находится в состоянии DEBUG, " \
                                                  "Пополнить ваш testnet кошелек можно в телеграм боте https://t.me/testgiver_ton_bot, " \
                                                  "передав адрес кошелька. Данное сообщение будет удалено после деплоя"
                print(wallet.address.to_string(*[True * 4 if settings.DEBUG else True * 3]))
                return data_response

    def get_account(self, data: dict):
        pass

    def create_transaction(self, data: dict):
        pass

    def _get_atomic_amount(self, amount: str, currency: str):
        pass

    def convert(self, amount: str, currency: str):
        pass

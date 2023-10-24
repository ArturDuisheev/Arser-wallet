from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from django.conf import settings
from tonsdk.utils import bytes_to_b64str
import asyncio
from wallet.api.ton.services.client import get_client
from tonsdk.provider import prepare_address
from pytonlib.tonlibjson import ExternalMessageNotAccepted
from wallet.api.services.base import get_field_in_dict_or_exception
from global_modules.exeptions import CodeDataException
from TonTools import Wallet, TonCenterClient
from tonsdk.contract.wallet import WalletContract

class TonService:
    """ Класс для работы с TON"""
    @classmethod
    async def get_balance(cls, account=None) -> dict:
        return {
            "url": "https://testnet.tonscan.org/ru"
        }

    @classmethod
    async def create_wallet(cls, data: dict):
        if not data.get("activate", False):
            mnemonics, _, _, wallet = Wallets.create(version=WalletVersionEnum.v3r2, workchain=0)
            return {
                "address": wallet.address.to_string(*[True * 4 if settings.DEBUG else True * 3]),
                "mnemonics": mnemonics
            }
        else:
            client = await get_client()
            get_field_in_dict_or_exception(data, "mnemonics", "Вы не указали mnemonics")
            try:
                _, _, _, wallet = Wallets.from_mnemonics(mnemonics=data.get("mnemonics"),version=WalletVersionEnum.v3r2, workchain=0)
            except ExternalMessageNotAccepted as e:
                raise CodeDataException(status=400, error="Неверный mnemonics")
            query = wallet.create_init_external_message()
            deploy_message = query["message"].to_boc(False)
            try:
                await client.raw_send_message(deploy_message)
                return {
                    "message": "success"
                }
            except ExternalMessageNotAccepted as e:
                print(e, 213231231)
                data_response = {
                    "message": "Wallet balance is null, please to replenish your wallet",
                    
                }
                if settings.DEBUG:
                    data_response["additional"] = "Данное сообщение вы видите т.к приложение находится в состоянии DEBUG, " \
                                                  "Пополнить ваш testnet кошелек можно в телеграм боте https://t.me/testgiver_ton_bot, " \
                                                  "передав адрес кошелька. Данное сообщение будет удалено после деплоя"
                print(wallet.address.to_string(*[True * 4 if settings.DEBUG else True * 3]))
                raise CodeDataException(status=400, error=data_response)

    @classmethod
    def get_account(cls, data: dict):
        try:
            return Wallets.from_mnemonics(mnemonics=data.get("mnemonics"),version=WalletVersionEnum.v3r2, workchain=0)
        except:
            raise CodeDataException(status=400, error="Неверный mnemonics")

    @classmethod
    async def get_seqno(cls, wallet):
        address = wallet.address.to_string(*[True * 4 if settings.DEBUG else True * 3])
        client = await get_client()
        data = client.raw_run_method(method='seqno', address=address, stack_data=[])
        print(data, 213213)


    @classmethod
    async def create_transaction(cls, amount, address, wallet: WalletContract):
        client = await get_client()
        
        transfer_query = wallet.create_transfer_message(to_addr=address, amount=amount, seqno=1)
        transfer_message = transfer_query["message"].to_boc(False)
        try:
            print(123213)
            data = await client.raw_send_message(transfer_message)
            return data
        except ExternalMessageNotAccepted as e:
            print(e)
            raise CodeDataException(error="Wallet gas is null", status=400)


    


    def _get_atomic_amount(self, amount: str, currency: str):
        pass

    def convert(self, amount: str, currency: str):
        pass

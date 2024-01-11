from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from django.conf import settings
from tonsdk.utils import bytes_to_b64str
import asyncio
from wallet.api.ton.services.client import get_client
from TonTools import Wallet
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
            client = get_client()
            get_field_in_dict_or_exception(data, "mnemonics", "Вы не указали mnemonics")
            try:
                _, _, _, wallet = Wallets.from_mnemonics(mnemonics=data.get("mnemonics"),
                                                         version=WalletVersionEnum.v3r2,
                                                         workchain=0)
            except ExternalMessageNotAccepted as e:
                raise CodeDataException(status=400, error="Неверный mnemonics")
            query = wallet.create_init_external_message()
            deploy_message = bytes_to_b64str(query["message"].to_boc(False))
            try:
                status = await client.send_boc(deploy_message)
                if status not in [200, 201]:
                    raise Exception()
                return {
                    "message": "success",
                    "address": wallet.address.to_string(*[True * 4 if settings.DEBUG else True * 3])
                }
            except Exception as e:
                print(e)
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
            
            return Wallet(mnemonics=data.get("mnemonics"), version='v3r2', provider=get_client())
        except:
            raise CodeDataException(status=400, error="Неверный mnemonics")

    @classmethod
    async def get_seqno(cls, wallet):
        address = wallet.address.to_string(*[True * 4 if settings.DEBUG else True * 3])
        client = get_client()
        data = client.raw_run_method(method='seqno', address=address, stack_data=[])
        print(data, 213213)


    @classmethod
    async def create_transaction(cls, amount, address, wallet: Wallet):
        try:
            transfer_query = await wallet.transfer_ton(destination_address=address, amount=amount)
            print(transfer_query)
            return {
                "@extra": "test_transaction"
            }
        except:
            return {
                "@extra": "test_transactions"
            }

    


    def _get_atomic_amount(self, amount: str, currency: str):
        pass

    def convert(self, amount: str, currency: str):
        pass

from wallet.api.btc.convert import BtcConverter
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from django.conf import settings
import asyncio
from wallet.api.btc.services.client import get_client
from tonsdk.provider import prepare_address
from pytonlib.tonlibjson import ExternalMessageNotAccepted
from wallet.api.services.base import get_field_in_dict_or_exception
from global_modules.exeptions import CodeDataException


class BtcService:
    """ Класс для работы с BTC"""



    @classmethod
    def get_balance(cls, account) -> dict:
        """
        Получить баланс аккаунта
        :param account:
        :return:
        """
        try:
            client = get_client(settings.BTC_WALLET_NAME)
            balance = client.getreceivedbyaddress(account)
            return {'balance': balance}
        except Exception as e:
            raise CodeDataException(f'Ошибка при получении баланса: {e}')

    @classmethod
    def create_wallet(cls, data: dict):
        
        client = get_client(settings.BTC_WALLET_NAME)
        address = client.getnewaddress()
        return address

    @classmethod
    def get_account(cls, data: dict):
        ...

    @classmethod
    def create_transaction(cls, amount, address):
        client = get_client(settings.BTC_WALLET_NAME)
        try:
            txid = client.sendtoaddress(address, amount)
            print(f'Отправлена транзакция {txid}')
            cls.generate_to_address(settings.BTC_DEFAULT_WALLET_ADDRESS)
            return {'txid': txid}
        except Exception as e:
            raise CodeDataException(f'Ошибка при отправке транзакции: {e}')

    def _get_atomic_amount(self, amount: str, currency: str):
        pass

    def convert(self, amount: str, currency: str):
        pass
    

    @classmethod
    def generate_to_address(cls, address):
        """
        'Намайнить' новую криптовалюту на выбранный адрес.
        {в нашем случае это необходмо, чтобы обновить информацию в regtest блокчейне} 
        """
        client = get_client(settings.BTC_WALLET_NAME)
        try:
            txid = client.generatetoaddress(1, address)
            print(f'Отправлена транзакция {txid}')
        except Exception as e:
            print(f'Ошибка при отправке транзакции: {e}')
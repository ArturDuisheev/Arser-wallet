import codecs
import json
from time import sleep

import base58
import requests
from hexbytes import HexBytes
from global_modules.exeptions import CodeDataException

from django.conf import settings
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import to_hex_address
from tronpy.keys import PrivateKey
from tronpy.contract import Contract
from tronpy.tron import TransactionBuilder, Transaction
from solc.main import get_solc_version

from wallet.choices import NetWorkChoice, CurrencyNetWorkChoice
from wallet.models import Wallet, Payment
from .abi import abi
from .bytecode import bytecode

client = Tron(network='nile')
# TRC20 лимит коммисии (ставить от 16, иначе транзакция может не пройти)
TRC20_FEE_LIMIT = 20_000_000  # Лимит 20 TRX

# 70a08231: balanceOf(address)
METHOD_BALANCE_OF = 'balanceOf(address)'

# a9059cbb: transfer(address,uint256)
METHOD_TRANSFER = 'transfer(address,uint256)'

TOKEN_USDT = 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj'


def address_to_parameter(addr):
    return "0" * 24 + base58.b58decode_check(addr)[1:].hex()


class UsdtTronService:

    @classmethod
    def get_balance(cls, account: str):
        from decimal import Decimal
        payload = {
            'owner_address': base58.b58decode_check(account).hex(),
            'contract_address': base58.b58decode_check(TOKEN_USDT).hex(),
            'function_selector': METHOD_BALANCE_OF,
            'parameter': address_to_parameter(account),
        }
        url = client.provider.endpoint_uri + '/wallet/triggerconstantcontract'
        resp = requests.post(url, json=payload)
        data = resp.json()

        val = data['constant_result'][0]
        return Decimal(int(val, 16) / 1_000_000)

    @classmethod
    def get_account(cls, address: str) -> dict:
        return address

    @classmethod
    def create_wallet(cls, **kwargs) -> str:
        wallet = client.generate_address_with_mnemonic()[0]
        Wallet.objects.create(
            network=NetWorkChoice.TRON,
            currency=CurrencyNetWorkChoice.USDT,
            order_id=1,
            address=wallet['base58check_address'],
            url_callback='1',
            priv_key=wallet['private_key']
        )
        print('create_tron_wallet_priv_key', wallet['private_key'], wallet['base58check_address'])
        return wallet['base58check_address']

    @classmethod
    def create_transaction(cls, from_address: str, to_address: str, amount: int):
        return send_usdt(from_address, to_address, amount)


def send_usdt(owner_address: str, to_address: str, amount: str):
    """
    send TRX amount is in SUN (smallest unit) from owner_addr to_addr
    """
    ABI = [{
        "outputs": [
            {
                "type": "bool"
            }
        ],
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "stateMutability": "Nonpayable",
        "type": "Function"
    }]
    from decimal import Decimal
    from_wallet = Wallet.objects.get(
        network=NetWorkChoice.TRON,
        address=owner_address
    )

    # print('wallet data: %r' % from_wallet)
    priv_key = PrivateKey(bytes.fromhex(from_wallet.priv_key))
    # amount = 1_000
    amount = Decimal(amount)
    amount = int(amount * 1_000_000)
    # amount = int(amount * (10**6))
    # amount = amount * 10 ** 6  # TRX amount is in SUN (smallest unit)
    print('Send: %s USDT' % (Decimal(amount) / 1_000_000))

    if (not client.is_base58check_address(to_address)):
        raise ValueError  # address provided is invalid

    contract = client.get_contract(TOKEN_USDT)
    contract.abi = ABI
    public_key_from = priv_key.public_key.to_base58check_address()
    assert public_key_from == owner_address

    txn = (
        contract.functions.transfer(to_address, amount)
        .with_owner(public_key_from)  # address of the private key
        .fee_limit(TRC20_FEE_LIMIT)
        .build()
        .sign(priv_key)
    )
    print(txn.txid)
    print(txn)

    txn_out = txn.broadcast()
    print(txn_out)
    print(txn_out.wait())
    from_wallet.save()
    print(from_wallet.balance)
    sleep(2)
    if Wallet.objects.filter(network=NetWorkChoice.TRON, currency=CurrencyNetWorkChoice.USDT,
                             address=to_address).exists():
        wallet = Wallet.objects.get(network=NetWorkChoice.TRON, currency=CurrencyNetWorkChoice.USDT,
                                    address=to_address)
        wallet.balance = UsdtTronService().get_balance(to_address)
        wallet.save()
    return txn.txid

from typing import List, Dict

from asgiref.sync import async_to_sync
from django.template import Library, Context

from admin_statistics.views import get_, get_converter, get_payment_amount_total
from wallet.choices import NetWorkChoice
from wallet.models import Wallet, Payment

register = Library()


@register.simple_tag(takes_context=True)
def get_admin_wallet(context: Context, using: str = "available_apps") -> List[Dict]:
    data = {

    }

    for network in NetWorkChoice.choices:
        print(network[0])
        try:
            wallet = Wallet.objects.get(network=network[0], is_admin=True)
        except:
            data[network[0]] = None
            continue
        converter = async_to_sync(get_converter)(network[0])
        params = {
            "fsyms": converter.spot,
            "tsyms": 'rub'
        }
        response_balance_rub = async_to_sync(get_)(params)
        balance_rub = response_balance_rub[converter.spot]['RUB']

        data[network[0]] = {
            "balance": {
                "coin": wallet.balance,
                "rub": wallet.balance * balance_rub
            },
            "address": wallet.address
        }
    return data


@register.simple_tag(takes_context=True)
def statistic(context: Context, using: str = "available_apps"):
    data = {
        'total_count': Payment.objects.count(),
        'total_sum': async_to_sync(get_payment_amount_total)()
    }
    return data
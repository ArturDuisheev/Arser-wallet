from collections.abc import Iterable

from django.forms import ValidationError
from wallet.choices import CurrencyChoice, NetWorkChoice, CurrencyNetWorkChoice
from django.db import models
from django.utils.translation import gettext_lazy as _

from reccuring.models import BaseModel


class Exchange(BaseModel):

    amount = models.DecimalField(
        max_digits=100,
        decimal_places=30,
        verbose_name=_("Сумма")
    )
    network = models.CharField(choices=NetWorkChoice.choices, max_length=10)
    network_from = models.CharField(choices=NetWorkChoice.choices, max_length=10)



class Payment(BaseModel):
    amount = models.DecimalField(
        max_digits=100,
        decimal_places=30,
        verbose_name=_("Сумма")
    )
    network = models.CharField(choices=NetWorkChoice.choices, max_length=10)
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=10)
    order_id = models.IntegerField(verbose_name=_("ID заказа"))
    address = models.CharField(max_length=200, verbose_name=_("Адрес"))
    url_callback = models.CharField(max_length=200, verbose_name=_("Ссылка"))


class Wallet(BaseModel):

    network = models.CharField(choices=NetWorkChoice.choices, max_length=10)
    currency = models.CharField(choices=CurrencyNetWorkChoice.choices, max_length=10)
    order_id = models.IntegerField(verbose_name=_("ID заказа"))
    address = models.CharField(max_length=200, verbose_name=_("Адрес"))
    balance = models.FloatField(blank=True, null=True, default=0)
    url_callback = models.CharField(max_length=200, verbose_name=_("Ссылка"))
    priv_key = models.TextField(blank=True, null=True)
    mnemonics = models.TextField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)


class WalletSettings(models.Model):
    count_commission = models.PositiveIntegerField(default=2)
from wallet.choices import CurrencyChoice, NetWorkChoice
from django.db import models
from django.utils.translation import gettext_lazy as _

from reccuring.models import BaseModel


class Payment(BaseModel):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Сумма")
    )
    network = models.CharField(choices=NetWorkChoice.choices, max_length=10)
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=10)
    order_id = models.IntegerField(verbose_name=_("ID заказа"))
    address = models.CharField(max_length=200, verbose_name=_("Адрес"))
    url_callback = models.CharField(max_length=200, verbose_name=_("Ссылка"))
<<<<<<< HEAD
=======
from collections.abc import Iterable

from django.forms import ValidationError
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
from wallet.choices import CurrencyChoice, NetWorkChoice
from django.db import models
from django.utils.translation import gettext_lazy as _

from reccuring.models import BaseModel


class Payment(BaseModel):
    amount = models.DecimalField(
<<<<<<< HEAD
        max_digits=10,
        decimal_places=6,
=======
        max_digits=100,
        decimal_places=2,
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
        verbose_name=_("Сумма")
    )
    network = models.CharField(choices=NetWorkChoice.choices, max_length=10)
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=10)
    order_id = models.IntegerField(verbose_name=_("ID заказа"))
    address = models.CharField(max_length=200, verbose_name=_("Адрес"))
<<<<<<< HEAD
    url_callback = models.CharField(max_length=200, verbose_name=_("Ссылка"))
=======
    url_callback = models.CharField(max_length=200, verbose_name=_("Ссылка"))

>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1

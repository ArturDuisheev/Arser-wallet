from collections.abc import Iterable

from django.forms import ValidationError
from wallet.choices import CurrencyChoice, NetWorkChoice
from django.db import models
from django.utils.translation import gettext_lazy as _

from reccuring.models import BaseModel


class Payment(BaseModel):
    amount = models.DecimalField(
        max_digits=100,
        decimal_places=2,
        verbose_name=_("Сумма")
    )
    network = models.CharField(choices=NetWorkChoice.choices, max_length=10)
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=10)
    order_id = models.IntegerField(verbose_name=_("ID заказа"))
    address = models.CharField(max_length=200, verbose_name=_("Адрес"))
    url_callback = models.CharField(max_length=200, verbose_name=_("Ссылка"))




class Tour(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))


class HoursDelta(BaseModel):
    hour_start = models.IntegerField(verbose_name=_("Начальная час"))
    hour_end = models.IntegerField(verbose_name=_("Конечная час"))

    def save(self, *args, **kwargs):
        if self.hour_end <= self.hour_start:
            raise ValidationError(_("Конечный час должен быть больше, чем начальный час"))
        
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.hour_start} - {self.hour_end}"


class TourDelta(BaseModel):

    price = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        verbose_name=_("Цена")
    )
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=10)
    hours_delta = models.ForeignKey(HoursDelta, on_delete=models.CASCADE, verbose_name=_("Длительность"))
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name=_("Тур"))

    

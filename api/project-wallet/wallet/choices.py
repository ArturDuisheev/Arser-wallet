from django.db import models


class NetWorkChoice(models.TextChoices):
    USDT = "USDT"
    BTC = "BTC"
    MONERO = "MONERO"
    TON = "TON"


class CurrencyChoice(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
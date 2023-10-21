from django.db import models


class NetWorkChoice(models.TextChoices):
    BTC = "BTC"
    MONERO = "MONERO"
    TON = "TON"
    TRON = "TRON"



class CurrencyNetWorkChoice(models.TextChoices):
    BTC = "BTC"
    MONERO = "MONERO"
    TON = "TON"
    USDT = "USDT"



class CurrencyChoice(models.TextChoices):
    USD = "USD"
    RUB = "RUB"
    BYN = "BYN"
    UAH = "UAH"
    KZT = "KZT"


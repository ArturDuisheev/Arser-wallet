from django.db import models


class NetWorkChoice(models.TextChoices):
    BTC = "BTC"
    MONERO = "MONERO"
    TON = "TON"
    TRON = "TRON"


class CurrencyChoice(models.TextChoices):
    USD = "USD"
<<<<<<< HEAD
    EUR = "EUR"
    RUB = "RUB"
=======
    RUB = "RUB"
    BYN = "BYN"
    UAH = "UAH"
    KZT = "KZT"
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1


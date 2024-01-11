

from django.forms import ValidationError
from monero import base58

class MoneroAddressValidator:

    length = (95, 106)

    def __call__(self, address: str):
        if len(address) not in self.length:
            raise ValidationError(f"Address must be between {self.length[0]} and {self.length[1]} characters")
        try:
            base58.decode(address)
        except:
            ...
            # raise ValidationError(f"Address must be a valid Monero address")
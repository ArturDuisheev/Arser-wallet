from wallet.api.validators import MoneroAddressValidator
from rest_framework import serializers


class MoneroGetBallanceSerializer(serializers.Serializer):

    account_index = serializers.IntegerField()


class MoneroTransactionSerializer(serializers.Serializer):
    
    account_index = serializers.IntegerField()
    amount = serializers.IntegerField()
    address = serializers.CharField(validators=[MoneroAddressValidator()])
from rest_framework import serializers

from wallet.api.validators import MoneroAddressValidator
from wallet import models as m_w


class MoneroDataSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = m_w.Payment
        fields = (
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')


class MoneroGetBallanceSerializer(serializers.Serializer):
    account_index = serializers.IntegerField()


class MoneroTransactionSerializer(serializers.Serializer):
    account_index = serializers.IntegerField()
    amount = serializers.IntegerField()
    address = serializers.CharField(validators=[MoneroAddressValidator()])

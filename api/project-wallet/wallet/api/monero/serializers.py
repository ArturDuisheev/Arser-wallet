from wallet.api.validators import MoneroAddressValidator
from rest_framework import serializers
from wallet import models as m_w

class NetworkSerializer(serializers.Serializer):

    network = serializers.CharField(max_length=100)




class PaymentDataSerializer(serializers.ModelSerializer):
    address = serializers.CharField()
    class Meta:
        model = m_w.Payment
        fields = [
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback'
        ]

class MoneroPaymentSerializer(PaymentDataSerializer):

    address = serializers.CharField(validators=[MoneroAddressValidator()])

    from_ = serializers.IntegerField()

    class Meta(PaymentDataSerializer.Meta):

        fields = [
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback', 'from_'
        ]


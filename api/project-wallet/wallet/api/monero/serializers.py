from wallet.api.validators import MoneroAddressValidator
from rest_framework import serializers
from wallet import models as m_w

class NetworkSerializer(serializers.Serializer):

    network = serializers.CharField(max_length=100)




class PaymentDataSerializer(serializers.ModelSerializer):
    address = serializers.CharField(validators=[MoneroAddressValidator()])
    class Meta:
        model = m_w.Payment
        fields = (
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback'
        )
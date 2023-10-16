from wallet.api.validators import MoneroAddressValidator
from rest_framework import serializers
from wallet import models as m_w

from wallet.choices import NetWorkChoice
class NetworkSerializer(serializers.Serializer):

    network = serializers.ChoiceField(choices=NetWorkChoice.choices)





class PaymentDataSerializer(serializers.ModelSerializer):
    address = serializers.CharField()
    class Meta:
        model = m_w.Payment
        fields = [
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback'
        ]


class MoneroCreateWalletSerializer(NetworkSerializer):
    label = serializers.CharField(max_length=100)
    activate = serializers.BooleanField()
    mnemonics = serializers.ListField(child=serializers.CharField())





class MoneroPaymentSerializer(PaymentDataSerializer):

    address = serializers.CharField(validators=[MoneroAddressValidator()])

    from_ = serializers.IntegerField(required=False)
    mnemonics = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta(PaymentDataSerializer.Meta):

        fields = [
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback', 'from_', 'mnemonics'
        ]



class QuerySeralizerGetBallance(NetworkSerializer):
    address = serializers.CharField(max_length=100, required=False)
    account_index = serializers.IntegerField(required=False)

    class Meta:
        fields = [
            'address', 'account_index'
        ]
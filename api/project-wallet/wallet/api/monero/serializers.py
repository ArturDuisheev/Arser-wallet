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
<<<<<<< HEAD
=======
    activate = serializers.BooleanField()
    mnemonics = serializers.ListField(child=serializers.CharField())


>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1



class MoneroPaymentSerializer(PaymentDataSerializer):

    address = serializers.CharField(validators=[MoneroAddressValidator()])

    from_ = serializers.IntegerField(required=False)
<<<<<<< HEAD
=======
    mnemonics = serializers.ListField(child=serializers.CharField(), required=False)
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1

    class Meta(PaymentDataSerializer.Meta):

        fields = [
<<<<<<< HEAD
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback', 'from_'
=======
            'id', 'amount', 'network', 'currency', 'order_id', 'address', 'url_callback', 'from_', 'mnemonics'
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
        ]



class QuerySeralizerGetBallance(NetworkSerializer):
    address = serializers.CharField(max_length=100, required=False)
    account_index = serializers.IntegerField(required=False)

    class Meta:
        fields = [
            'address', 'account_index'
        ]
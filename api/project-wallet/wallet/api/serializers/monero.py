from rest_framework import serializers


class MoneroGetBallanceSerializer(serializers.Serializer):

    account_index = serializers.IntegerField()
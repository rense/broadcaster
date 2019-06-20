from rest_framework import serializers


class ConnectionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        fields = [
            'id',
        ]


class MessageSerializer(serializers.Serializer):
    action = serializers.CharField(read_only=True)

    code = serializers.IntegerField(read_only=True)
    data = serializers.JSONField(required=False)

    class Meta:
        fields = [
            'action',
            'code',
            'data'
        ]

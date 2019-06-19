from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    code = serializers.IntegerField(read_only=True)
    data = serializers.JSONField(required=False)

    class Meta:
        fields = [
            'code',
            'data'
        ]


from rest_framework import serializers


class CartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(allow_null=False, allow_blank=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
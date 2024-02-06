from rest_framework import serializers
from shopping.models import *


class ItemSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=False)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    cost = serializers.FloatField()

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()
        return instance

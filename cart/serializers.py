from rest_framework import serializers
from cart.models import Order
from cart.repositories.orders_repo import add_to_cart, set_cart_quantity


class CartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(allow_null=False)

    def create(self, validated_data):
        return add_to_cart(
            order=validated_data.get('order'),
            item=validated_data.get('item'),
            quantity=validated_data.get('quantity')
        )

    def update(self, instance, validated_data):
        return set_cart_quantity(
            cart_item=validated_data.get('cart'),
            quantity=validated_data.get('quantity')
        )
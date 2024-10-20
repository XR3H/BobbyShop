from rest_framework import serializers
from cart.models import Order, CartItem
from cart.repositories.orders_repo import add_to_cart, set_cart_quantity
from catalog.models import Item

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


class ItemMinimumReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'title', 'cost')

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ('order',)
        depth = 1

class CartOrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        depth = 1
        exclude = ('client', 'uuid')
        # fields = '__all__'
    cartitem_set = CartItemSerializer(many=True, read_only=True)

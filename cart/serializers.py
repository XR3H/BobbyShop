from rest_framework import serializers
from cart.models import Order, CartItem
from cart.repositories.orders_repo import set_cart_quantity, get_cart_item
from catalog.models import Item

class CartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(allow_null=False)

    def create(self, validated_data):
        order = validated_data.get('order')
        item = validated_data.get('item')
        add_quantity = validated_data.get('quantity')
        cart_item, _ = get_cart_item(
            order=order, item=item
        )
        cart_item.quantity += add_quantity
        cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity')
        instance.save()
        return instance


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

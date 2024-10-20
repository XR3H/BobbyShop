from django.shortcuts import render
import rest_framework.views as views
from rest_framework.response import Response
from rest_framework import status
from catalog.permissions import *
from cart.serializers import *
from cart.repositories.orders_repo import *
from catalog.repositories.items_repo import get_item


# Create your views here.

class CartView(views.APIView):
    # permission_classes = [, ]

    def post(self, request, id=None):
        item = None
        try:
            item = get_item(id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid id'})
        cart_item_data = CartSerializer(data=request.data)
        if not cart_item_data.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Data is not valid!"})

        try:
            order = prepare_cart_order(
                client=request.user,
                uuid=request.headers.get('UUID')
            )
            cart_item_data.save(order=order, item=item)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"Error during cart refilling!\n{e}"})

        return Response(status=status.HTTP_200_OK, data={'message': 'OK'})

    def put(self, request, id=None):
        item = None
        try:
            item = get_item(id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid id'})
        order = prepare_cart_order(
            client=request.user,
            uuid=request.headers.get('UUID')
        )
        cart_item = CartItem.objects.get(order=order, item=item)
        cart_item_data = CartSerializer(instance=cart_item, data=request.data)
        if not cart_item_data.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Data is not valid!"})
        cart_item_data.save(cart=cart_item)
        return Response(status=status.HTTP_200_OK, data={'message': 'OK'})

    def get(self, request):
        cart_order = prepare_cart_full(
            client=request.user,
            uuid=request.headers.get('UUID')
        )
        cart_order_data = CartOrderReadSerializer(cart_order)
        return Response(status=status.HTTP_200_OK, data={"data": cart_order_data.data})

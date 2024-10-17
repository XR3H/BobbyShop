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

        client = request.user
        uuid = request.headers.get('UUID')

        order = prepare_cart_order(client=client, uuid=uuid)
        cart_item_data.save(order=order, item=item)

        return Response(status=status.HTTP_200_OK, data={'message': 'OK'})

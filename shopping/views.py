import django.http
from django.core import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping.models import *
from shopping.serializers import *
from rest_framework.viewsets import *
import rest_framework.permissions as permissions
from shopping.repositories import items_repo

# Create your views here.

class ItemView(APIView):
    def get(self, request, id=None):
        data = None
        if(not id):
            # Spread logit to whole project
            items_data = ItemReadSerializer(
                items_repo.all_items_with_attributes(),
                many=True
            )
            return Response( status=status.HTTP_200_OK, data={"data":items_data.data} )
        try:
            item = items_repo.get_item_with_attributes(id)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={ 'message': 'Invalid id' })

        item_data = ItemReadSerializer(item)
        return Response(status=status.HTTP_200_OK, data={'data': item_data.data})

    def post(self, request):
        item_data = ItemSerializer(data=request.data)
        try:
            item_data.is_valid()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Data is not valid!"})
        try:
            item_data = ItemReadSerializer(
                items_repo.get_item_with_attributes( item_data.save().id )
            )
        except:
            return Response(status=status.HTTP_200_OK, data={"message": "Invalid data provided!"})
        return Response(status=status.HTTP_200_OK, data={'data':item_data.data})

    def put(self, request, id=None):
        if not id:
            return Response("No item id stated in request!")
        try:
            item = items_repo.get_item(id)
        except Exception:
            return Response( status=status.HTTP_400_BAD_REQUEST, data={"message": f"No item with id={id}!"} )
        item_data = ItemSerializer(instance=item, data=request.data)
        try:
            item_data.is_valid()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Data is not valid!"})
        try:
            item_data = ItemReadSerializer( item_data.save() )
        except Exception:
            return Response(status=status.HTTP_200_OK, data={"message": "Invalid data provided!"})
        return Response( status=status.HTTP_200_OK, data={"message": item_data.data} )

    def delete(self, request, id=None):
        if not id:
            return Response("No item id stated in request!")
        try:
            item = items_repo.get_item(id)
        except Exception:
            return Response( status=status.HTTP_400_BAD_REQUEST, data={"message" : f"No item with id={id}"} )
        item.delete()
        return Response( status=status.HTTP_200_OK, data={"message" : "Item was successfully deleted"} )

# class CatalogueView(ListAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemReadSerializer
#     permission_classes = (permissions.AllowAny,)
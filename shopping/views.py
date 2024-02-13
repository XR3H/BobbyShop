import django.http
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping.models import *
from shopping.serializers import *
from rest_framework.viewsets import *
import rest_framework.permissions as permissions

# Create your views here.

class ItemView(APIView):
    def get(self, request, id=None):
        data = None
        if(not id):
            items_data = ItemReadSerializer( Item.objects.all(), many=True )
            return Response( status=status.HTTP_200_OK, data={"data":items_data.data} )
        try:
            item = Item.objects.get(id=id)
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
            item_data = ItemReadSerializer( item_data.save() )
        except:
            return Response(status=status.HTTP_200_OK, data={"message": "Invalid data provided!"})
        return Response(status=status.HTTP_200_OK, data={'data':item_data.data})

    def put(self, request, id=None):
        if not id:
            return Response("No item id stated in request!")
        try:
            item = Item.objects.get(id=id)
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
            item = Item.objects.get(id=id)
        except Exception:
            return Response( status=status.HTTP_400_BAD_REQUEST, data={"message" : f"No item with id={id}"} )
        item.delete()
        return Response( status=status.HTTP_200_OK, data={"message" : "Item was successfully deleted"} )

# class CatalogueView(ListAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemReadSerializer
#     permission_classes = (permissions.AllowAny,)
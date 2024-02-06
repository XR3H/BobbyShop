import django.http
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping.models import *
from shopping.serializers import *

# Create your views here.

class ItemView(APIView):
    def get(self, request):
        item_list = Item.objects.all()
        return Response(status=status.HTTP_200_OK, data={'data':ItemSerializer(item_list, many=True).data})

    def post(self, request):
        item = ItemSerializer(data=request.data)
        try:
            item.is_valid()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Data is not valid!"})
        item.save()
        return Response(status=status.HTTP_200_OK, data={'data':item.data})
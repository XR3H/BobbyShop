from django.shortcuts import render
import rest_framework.views as views
from rest_framework.response import Response
from rest_framework import status
from catalog.permissions import *


# Create your views here.

class CartView(views.APIView):
    # permission_classes = [, ]

    def post(self, request):
        client = request.user
        uuid = request.headers.get('UUID')

        return Response(status=status.HTTP_200_OK, data={'message': 'OK'})

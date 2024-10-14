from django.urls import path
from cart.views import *

urlpatterns = [
    path('cart/', CartView.as_view())
]
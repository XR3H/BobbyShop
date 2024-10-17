from django.urls import path
from cart.views import *

urlpatterns = [
    path('cart/<int:id>/', CartView.as_view())
]
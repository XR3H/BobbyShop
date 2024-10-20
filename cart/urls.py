from django.urls import path
from cart.views import *

urlpatterns = [
    path('cart/<int:id>/', CartView.as_view()),
    path('cart/', CartView.as_view())
]
from django.urls import path

from shopping.views import ItemView

urlpatterns = [
    path('yes/', ItemView.as_view()),
]

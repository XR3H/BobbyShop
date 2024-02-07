from django.urls import path

from shopping.views import ItemView#, CatalogueView

urlpatterns = [
    path('item/<int:id>', ItemView.as_view()),
    path('item/', ItemView.as_view()),

    # path('catalogue/', CatalogueView.as_view()),
]

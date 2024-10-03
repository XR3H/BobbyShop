from django.urls import path
import rest_framework.routers as routers
from shopping.views import *

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, 'categories')

urlpatterns = [
    path('item/<int:id>', ItemView.as_view()),
    path('item/', ItemView.as_view()),


    # path('catalogue/', CatalogueView.as_view()),
]

urlpatterns += router.urls

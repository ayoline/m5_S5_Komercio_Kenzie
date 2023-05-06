from django.urls import path
from products.views import ListCreateProducts, ListUpdateProduct

urlpatterns = [
    path("products/", ListCreateProducts.as_view()),
    path("products/<pk>/", ListUpdateProduct.as_view()),
]

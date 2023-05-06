from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Product
from .serializers import ProductSerializer, ProductSerializerCommon
from rest_framework.authentication import TokenAuthentication
from .permissions import IsGetorSeller, IsOwner
from utils.mixins import SerializerByMethodMixin
import ipdb


class ListCreateProducts(SerializerByMethodMixin, ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsGetorSeller]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializerCommon,
        "POST": ProductSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ListUpdateProduct(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

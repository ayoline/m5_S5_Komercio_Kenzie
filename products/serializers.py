from rest_framework import serializers
from accounts.serializers import AccountSerializer
from .models import Product


class ProductSerializerCommon(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
        read_only_fields = ["seller_id"]


class ProductSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["seller"]

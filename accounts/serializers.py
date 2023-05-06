from rest_framework import serializers
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = [
            "date_joined",
            "is_superuser",
            "is_active",
        ]

    def create(self, validated_data: dict):
        user_obj = Account.objects.create_user(**validated_data)

        return user_obj


class AccountSoftDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = [
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

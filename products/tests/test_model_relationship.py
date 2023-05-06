from django.test import TestCase
from products.models import Product
from accounts.models import Account


class ProductRelationshipTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_data = {
            "username": "seller",
            "password": "1234",
            "first_name": "seller1",
            "last_name": "seller1",
            "is_seller": True,
        }

        cls.product_data = {
            "description": "teste",
            "price": 12.12,
            "quantity": 5,
        }

        cls.account = Account.objects.create_user(**cls.account_data)
        cls.product = Product.objects.create(**cls.product_data, seller=cls.account)

    def test_many_to_one_relationship(self):
        """
        Verifica o relacionamento entre produto e seller
        """
        expected_seller_username = "seller"
        result_seller_username = self.product.seller.username
        msg = f"Verifique se o valor de `seller` foi definida como {expected_seller_username}"

        self.assertEqual(expected_seller_username, result_seller_username, msg)

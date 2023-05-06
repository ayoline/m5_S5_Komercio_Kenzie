from django.test import TestCase
from products.models import Product
from accounts.models import Account


class ProductModelTest(TestCase):
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

    def test_id_primary_key(self):
        """
        Verifica a propriedade primary_key de `id`
        """
        expected_primary_key = True
        result_primary_key = Product._meta.get_field("id").primary_key
        msg = f"Verifique se a propriedade `primary_key` de id foi definida como {expected_primary_key}"

        self.assertEqual(expected_primary_key, result_primary_key, msg)

    def test_id_editable(self):
        """
        Verifica a propriedade editable de `id`
        """
        expected_editable = False
        result_editable = Product._meta.get_field("id").editable
        msg = f"Verifique se a propriedade `editable` de id foi definida como {expected_editable}"

        self.assertEqual(expected_editable, result_editable, msg)

    def test_is_active_default(self):
        """
        Verifica a propriedade default de `is_active`
        """
        expected_default = True
        result_default = Product._meta.get_field("is_active").default
        msg = f"Verifique se a propriedade `default` de is_active foi definida como {expected_default}"

        self.assertEqual(expected_default, result_default, msg)

    def test_price_max_digits(self):
        """
        Verifica a propriedade max_digits de `price`
        """
        expected_max_digits = 10
        result_max_digits = Product._meta.get_field("price").max_digits
        msg = f"Verifique se a propriedade `max_digits` de price foi definida como {expected_max_digits}"

        self.assertEqual(expected_max_digits, result_max_digits, msg)

    def test_price_decimal_places(self):
        """
        Verifica a propriedade max_digits de `price`
        """
        expected_decimal_places = 2
        result_decimal_places = Product._meta.get_field("price").decimal_places
        msg = f"Verifique se a propriedade `decimal_places` de price foi definida como {expected_decimal_places}"

        self.assertEqual(expected_decimal_places, result_decimal_places, msg)

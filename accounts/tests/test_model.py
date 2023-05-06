from django.test import TestCase
from accounts.models import Account
from django.core.exceptions import ValidationError


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_data = {
            "username": "seller",
            "password": 1234,
            "first_name": "seller1",
            "last_name": "seller1",
            "is_seller": True,
        }

        cls.account = Account.objects.create(**cls.account_data)

    def test_id_primary_key(self):
        """
        Verifica a propriedade primary_key de `id`
        """
        expected_primary_key = True
        result_primary_key = Account._meta.get_field("id").primary_key
        msg = f"Verifique se a propriedade `primary_key` de id foi definida como {expected_primary_key}"

        self.assertEqual(expected_primary_key, result_primary_key, msg)

    def test_username_max_length(self):
        """
        Verifica a propriedade de tamanho máximo de `username`
        """
        expected_max_length = 20
        result_max_length = Account._meta.get_field("username").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result_max_length, msg)

    def test_if_duplicated_username_can_be_created(self):
        account_data = {
            "username": self.account.username,
            "password": 1234,
            "first_name": "seller1",
            "last_name": "seller1",
            "is_seller": True,
        }

        account = Account(**account_data)
        expected_message = "User with this Username already exists."
        with self.assertRaisesMessage(ValidationError, expected_message):
            account.full_clean()

    def test_id_editable(self):
        """
        Verifica a propriedade primary_key de `id`
        """
        expected_editable = False
        result_editable = Account._meta.get_field("id").editable
        msg = f"Verifique se a propriedade `editable` de id foi definida como {expected_editable}"

        self.assertEqual(expected_editable, result_editable, msg)

    def test_first_name_max_length(self):
        """
        Verifica a propriedade de tamanho máximo de `first_name`
        """
        expected_max_length = 50
        result_max_length = Account._meta.get_field("first_name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result_max_length, msg)

    def test_last_name_max_length(self):
        """
        Verifica a propriedade de tamanho máximo de `last_name`
        """
        expected_max_length = 50
        result_max_length = Account._meta.get_field("last_name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result_max_length, msg)

    def test_is_seller_default(self):
        """
        Verifica a propriedade default de `is_seller`
        """
        expected_default = False
        result_default = Account._meta.get_field("is_seller").default
        msg = f"Verifique se a propriedade `default` de is_seller foi definida como {expected_default}"

        self.assertEqual(expected_default, result_default, msg)

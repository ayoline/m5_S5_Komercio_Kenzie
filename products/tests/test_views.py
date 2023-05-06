from accounts.models import Account
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
import ipdb


class ProductsTestView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_data = {
            "username": "normal",
            "password": "1234",
            "first_name": "ander",
            "last_name": "son",
            "is_seller": False,
        }

        user_data1 = {
            "username": "seller",
            "password": "1234",
            "first_name": "ander",
            "last_name": "son",
            "is_seller": True,
        }

        user_data2 = {
            "username": "admin",
            "password": "1234",
            "first_name": "ander",
            "last_name": "son",
            "is_seller": False,
        }

        cls.product_data = {
            "description": "teste",
            "price": 12.12,
            "quantity": 5,
        }

        cls.normaluser = Account.objects.create_user(**user_data)
        cls.seller = Account.objects.create_user(**user_data1)
        cls.admin = Account.objects.create_superuser(**user_data2)

    def test_if_only_seller_can_create_products(self):
        """
        Verifica se apenas o vendedor pode criar um produto
        """
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_admin = self.client.post(f"/api/products/", self.product_data)
        self.assertEqual(403, res_admin.status_code)

        token = Token.objects.create(user=self.normaluser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_normal = self.client.post(f"/api/products/", self.product_data)
        self.assertEqual(403, res_normal.status_code)

        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_seller = self.client.post(f"/api/products/", self.product_data)
        self.assertEqual(201, res_seller.status_code)

    def test_if_only_owner_can_update_product(self):
        """
        Verifica se apenas o criador do produto pode atualizar ele
        """
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_product = self.client.post("/api/products/", self.product_data)

        res_owner = self.client.patch(
            f'/api/products/{res_product.data["id"]}/', {"price": 999}
        )
        self.assertEqual(200, res_owner.status_code)

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_admin = self.client.patch(
            f'/api/products/{res_product.data["id"]}/', {"price": 999}
        )
        self.assertEqual(403, res_admin.status_code)

        token = Token.objects.create(user=self.normaluser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_normal = self.client.patch(
            f'/api/products/{res_product.data["id"]}/', {"price": 999}
        )
        self.assertEqual(403, res_admin.status_code)

    def test_if_anyone_can_list_and_filter_product(self):
        """
        Verifica se qualquer um pode listar e filtrar produtos
        """
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_product = self.client.post("/api/products/", self.product_data)

        self.client.credentials(HTTP_AUTHORIZATION="")
        res_list = self.client.get("/api/products/")
        self.assertEqual(200, res_list.status_code)

        res_filter = self.client.get(f'/api/products/{res_product.data["id"]}/')
        self.assertEqual(200, res_filter.status_code)

    def test_if_can_create_product_with_negative_quantity(self):
        """
        Verifica se é possível criar um produto com quantidade negativa
        """
        product_data = {
            "description": "teste",
            "price": 12.12,
            "quantity": -1,
        }

        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_product = self.client.post("/api/products/", product_data)

        self.assertIn(
            "Ensure this value is greater than or equal to 0.",
            res_product.data["quantity"],
        )

    def test_if_can_create_product_with_wrong_key(self):
        """
        Verica se é possível criar um produto com chaves erradas
        """
        product_data = {
            "description": "teste",
            "price": 12.12,
            "wrong_key": 1,
        }

        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_product = self.client.post("/api/products/", product_data)
        self.assertEqual(400, res_product.status_code)

    def test_if_exists_especific_return_to_create_product(self):
        """
        Verifica se existe uma saída expecifica para a criação de produtos
        """
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_product = self.client.post("/api/products/", self.product_data)

        expected_keys = {
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        }
        result_keys = set(res_product.data.keys())
        self.assertEqual(expected_keys, result_keys)

    def test_if_exists_especific_return_to_list_product(self):
        """
        Verifica se existe um retorno específico para a listagem de produtos
        """
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.client.post("/api/products/", self.product_data)
        res_product = self.client.get("/api/products/")

        expected_keys = {"is_active", "price", "seller_id", "quantity", "description"}
        result_keys = set(res_product.data.get("results")[0].keys())
        self.assertEqual(expected_keys, result_keys)


# ipdb.set_trace()
# print()

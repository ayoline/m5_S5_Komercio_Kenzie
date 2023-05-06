from accounts.models import Account
from rest_framework.views import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse


class AccountSellerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.account_data = {
            "username": "seller",
            "password": "1234",
            "first_name": "seller",
            "last_name": "seller",
            "is_seller": True,
        }

        cls.account = Account.objects.create_user(**cls.account_data)

    def test_if_seller_account_was_created(self):
        """
        Verifica se uma conta de vendedor foi criada
        """
        expected_value = True
        result_value = self.account.is_seller
        msg = "Verifique o porque a conta de vendedor não pode ser criada"

        self.assertEqual(expected_value, result_value, msg)


class AccountNonSellerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.account_data = {
            "username": "seller",
            "password": "1234",
            "first_name": "seller",
            "last_name": "seller",
            "is_seller": False,
        }

        cls.account = Account.objects.create_user(**cls.account_data)

    def test_if_non_seller_account_was_created(self):
        """
        Verifica se uma conta normal foi criada
        """
        expected_value = False
        result_value = self.account.is_seller
        msg = "Verifique o porque a conta não pode ser criada"

        self.assertEqual(expected_value, result_value, msg)


class AccountSellerErrorKeyTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.account_data = {
            "username": "seller",
            "password": "1234",
            "wrong_key": "seller",
            "last_name": "seller",
            "is_seller": True,
        }

    def test_can_register_seller_account_with_wrong_key(self):
        """
        Verifica se uma conta de vendedor com chaves erradas pode ser registrada
        """
        response = self.client.post(self.register_url, self.account_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = "Verifique se a conta foi criada com a chave errada do mesmo jeito"

        self.assertEqual(expected_status_code, result_status_code, msg)


class AccountNonSellerErrorKeyTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.account_data = {
            "username": "seller",
            "password": "1234",
            "wrong_key": "seller",
            "last_name": "seller",
            "is_seller": False,
        }

    def test_can_register_non_seller_account_with_wrong_key(self):
        """
        Verifica se uma conta normal com chaves erradas pode ser registrada
        """
        response = self.client.post(self.register_url, self.account_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = "Verifique se a conta foi criada com a chave errada do mesmo jeito"

        self.assertEqual(expected_status_code, result_status_code, msg)


class AccountSellerLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("login")
        user_data = {
            "username": "seller",
            "password": "1234",
            "first_name": "seller",
            "last_name": "seller",
            "is_seller": True,
        }

        cls.user_login = {
            "username": "seller",
            "password": "1234",
        }

        user = Account.objects.create_user(**user_data)

    def test_can_seller_login_generate_token(self):
        """
        Verifica se um login de vendedor está gerando o token
        """
        login = self.client.post(self.login_url, data=self.user_login)

        self.assertIn("token", login.data)


class AccountNormalUserLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("login")
        user_data = {
            "username": "normaluser",
            "password": "1234",
            "first_name": "seller",
            "last_name": "seller",
            "is_seller": False,
        }

        cls.user_login = {
            "username": "normaluser",
            "password": "1234",
        }

        user = Account.objects.create_user(**user_data)

    def test_can_normal_user_login_generate_token(self):
        """
        Verifica se um login normal está gerando o token
        """
        login = self.client.post(self.login_url, data=self.user_login)

        self.assertIn("token", login.data)


class AccountPermissionsTest(APITestCase):
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
            "username": "user",
            "password": "1234",
            "first_name": "ander",
            "last_name": "son",
            "is_seller": False,
        }

        cls.normaluser = Account.objects.create_user(**user_data)
        cls.seller = Account.objects.create_user(**user_data1)
        cls.admin = Account.objects.create_superuser(**user_data2)

    def test_if_only_owner_can_update_user(self):
        """
        Verifica se apenas o criador pode atualizar a conta
        """
        token = Token.objects.create(user=self.normaluser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        res_owner = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/", {"first_name": "ander Patched"}
        )
        self.assertIn("ander Patched", res_owner.data["first_name"])

        res_otheruser = self.client.patch(
            f"/api/accounts/{str(self.seller.id)}/", {"first_name": "ander Patched"}
        )
        self.assertEqual(403, res_otheruser.status_code)

        res_admin = self.client.patch(
            f"/api/accounts/{str(self.admin.id)}/", {"first_name": "ander Patched"}
        )
        self.assertEqual(403, res_admin.status_code)

    def test_if_only_admin_can_deactivate_account(self):
        """
        Verifica se apenas o admin pode desativar uma conta
        """
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_admin = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/management/", {"is_active": False}
        )
        self.assertEqual(200, res_admin.status_code)

        token = Token.objects.create(user=self.normaluser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_normal = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/management/", {"is_active": False}
        )
        self.assertEqual(401, res_normal.status_code)

        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_seller = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/management/", {"is_active": False}
        )
        self.assertEqual(403, res_seller.status_code)

    def test_if_only_admin_can_reactivate_account(self):
        """
        Verifica se apenas o admin pode reativar um conta
        """
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_admin = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/management/", {"is_active": True}
        )
        self.assertEqual(200, res_admin.status_code)

        token = Token.objects.create(user=self.normaluser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_normal = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/management/", {"is_active": True}
        )
        self.assertEqual(403, res_normal.status_code)

        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res_seller = self.client.patch(
            f"/api/accounts/{str(self.normaluser.id)}/management/", {"is_active": True}
        )
        self.assertEqual(403, res_seller.status_code)

    def test_if_anyone_can_list_all_accounts(self):
        """
        Verifica se qualquer um pode listar todos os usuários
        """
        response = self.client.get("/api/accounts/")
        self.assertEqual(200, response.status_code)

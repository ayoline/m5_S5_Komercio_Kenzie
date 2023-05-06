from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response, Request, status
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from accounts.models import Account
from accounts.serializers import AccountSerializer, AccountSoftDeleteSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema


class LoginView(ObtainAuthToken):
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountFilterView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        number_of_accounts = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:number_of_accounts]


class AccountUpdateView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountUpdateSoftDeleteView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Account.objects.all()
    serializer_class = AccountSoftDeleteSerializer

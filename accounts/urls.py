from django.urls import path
from .views import (
    LoginView,
    AccountView,
    AccountFilterView,
    AccountUpdateView,
    AccountUpdateSoftDeleteView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("accounts/<pk>/", AccountUpdateView.as_view(), name="update_user"),
    path("accounts/<pk>/management/", AccountUpdateSoftDeleteView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("accounts/newest/<int:num>/", AccountFilterView.as_view()),
    # Acessa o download do schema
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Opcionais
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]

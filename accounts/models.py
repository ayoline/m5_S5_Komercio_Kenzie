from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Account(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name"]

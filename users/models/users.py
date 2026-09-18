from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import USER_ROLES, ROLE_CUSTOMER


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default=ROLE_CUSTOMER,
    )
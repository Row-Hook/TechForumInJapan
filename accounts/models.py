from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """拡張ユーザモデル"""

    class Meta:
        app_label = 'accounts'
        verbose_name_plural = 'CustomUser'

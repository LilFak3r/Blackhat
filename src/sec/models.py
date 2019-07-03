from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthKey(models.Model):
    class Meta:
        verbose_name = "AuthKey"
        verbose_name_plural = "AuthKeys"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="two_fa")
    auth_key = models.CharField(max_length=16)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    enabled = models.BooleanField()

    def __str__(self):
        return f"Auth_key for [{self.user.username}]"
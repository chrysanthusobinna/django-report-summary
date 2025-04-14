from django.db import models
import secrets

class ClientAPIKey(models.Model):
    name = models.CharField(max_length=100, unique=True)
    key = models.CharField(max_length=40, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

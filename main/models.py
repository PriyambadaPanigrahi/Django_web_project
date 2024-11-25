from django.db import models
import uuid

class Account(models.Model):
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=64, unique=True)
    website = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_name


class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="destinations")
    url = models.URLField()
    http_method = models.CharField(choices=(('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')), max_length=10)
    headers = models.JSONField()

    def __str__(self):
        return self.url


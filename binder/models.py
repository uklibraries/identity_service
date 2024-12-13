from django.db import models
from minter.models import Naan


class Role(models.Model):
    naan = models.ForeignKey(Naan, null=True, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, default="unnamed")


class Ark(models.Model):
    role = models.ForeignKey(Role, null=True, on_delete=models.RESTRICT)
    identifier = models.CharField(max_length=255, default="unidentified")
    metadata = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "role"], name="unique_identifier_role_combination"
            )
        ]

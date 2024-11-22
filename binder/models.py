from django.db import models
from minter.models import Naan

class Role(models.Model):
    naan = models.ForeignKey(Naan, null=True, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, default="unnamed")

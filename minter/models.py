from django.db import models


class Naan(models.Model):
    number = models.IntegerField(unique=True, default=0)
    organization = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)

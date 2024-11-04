from django.db import models


class Naan(models.Model):
    id = models.IntegerField(primary_key=True)
    organization = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)

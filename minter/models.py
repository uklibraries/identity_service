from django.db import models
import json
import noid_minter.minter as nm


class Naan(models.Model):
    number = models.IntegerField(unique=True, default=0)
    organization = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)


class Minter(models.Model):
    naan = models.ForeignKey(Naan, null=True, on_delete=models.RESTRICT)
    shoulder = models.CharField(unique=True, default="tv", max_length=5)
    template = models.CharField(unique=True, default="tv.sddd", max_length=64)
    state = models.JSONField(default=dict)

    def _initial_state(self):
        return json.loads(nm.Minter(
            {"template": self.template, "naan": str(self.naan.number)}
        ).to_json())

    def save(self, *args, **kwargs):
        if not self.state:
            self.state = self._initial_state()
        super(Minter, self).save(*args, **kwargs)

    def mint(self):
        configuration = self.state
        nm_minter = nm.Minter(configuration)
        ark = nm_minter.mint().ark
        self.state = json.loads(nm_minter.to_json())
        return ark

from django.test import TestCase
from minter.models import Naan, Minter
import noid_minter.minter as nm


class NaanModelTest(TestCase):
    def setUp(self):
        Naan.objects.create(
            number=16417, organization="University of Kentucky Libraries", abbreviation="UKL"
        )

    def test_organization(self):
        naan = Naan.objects.get(number=16417)
        field_label = naan._meta.get_field("organization").verbose_name
        self.assertEqual(field_label, "organization")

    def test_abbreviation(self):
        naan = Naan.objects.get(number=16417)
        field_label = naan._meta.get_field("abbreviation").verbose_name
        self.assertEqual(field_label, "abbreviation")


class MinterModelTest(TestCase):
    def setUp(self):
        Naan.objects.create(
            number=16417, organization="University of Kentucky Libraries", abbreviation="UKL"
        )
        Minter.objects.create(
            naan=Naan.objects.get(number=16417), shoulder="tv", template="tv.sddd"
        )

    def test_state_uses_noid_minter(self):
        db_minter = Minter.objects.get(shoulder="tv")
        nm_minter = nm.Minter({"template": "tv.sddd", "naan": "16417"})
        got_ark = db_minter.mint()
        expected_ark = nm_minter.mint().ark
        assert got_ark == expected_ark

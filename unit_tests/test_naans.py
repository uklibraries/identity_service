from django.test import TestCase
from minter.models import Naan


class NaanModelTest(TestCase):
    def setUp(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )

    def test_organization(self):
        naan = Naan.objects.get(id=16417)
        field_label = naan._meta.get_field("organization").verbose_name
        self.assertEqual(field_label, "organization")

    def test_abbreviation(self):
        naan = Naan.objects.get(id=16417)
        field_label = naan._meta.get_field("abbreviation").verbose_name
        self.assertEqual(field_label, "abbreviation")

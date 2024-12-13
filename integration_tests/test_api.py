import pytest

from django.urls import reverse
from rest_framework import status
from minter.models import Naan, Minter
from binder.models import Ark, Role
from integration_tests.mixins import ApiJwtTestCase


class RootTests(ApiJwtTestCase):
    def setUp(self):
        self.authenticate()
        self.url = reverse("root")
        self.response = self.client.get(self.url, format="json")

    def test_root_returns_json(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        # Consider application/vnd.api+json.
        self.assertEqual(self.response.headers.get("Content-Type"), "application/json")

    def test_root_includes_relevant_links(self):
        self.assertIn("links", self.response.data)
        links = self.response.data["links"]
        self.assertEqual(links["self"], self.url)
        self.assertEqual(links["naans"], reverse("naans"))


class NaanTests(ApiJwtTestCase):
    def setUp(self):
        self.authenticate()

    def tearDown(self):
        self.assertEqual(self.response.data["links"]["self"], self.url)

    def test_create_naan(self):
        self.url = reverse("naans")
        data = {
            "number": 37,
            "organization": "University of Kentucky",
            "abbreviation": "UKY",
        }
        self.response = self.client.post(self.url, data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Naan.objects.count(), 1)
        self.assertEqual(Naan.objects.get().organization, "University of Kentucky")

    def test_retrieve_naan(self):
        Naan.objects.create(
            number=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.url = reverse("view-naan", kwargs={"number": 16417})
        self.response = self.client.get(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        data = self.response.data["data"]
        assert data["number"] == 16417
        assert data["organization"] == "University of Kentucky"
        assert data["abbreviation"] == "UKY"

    def test_partial_update_naan(self):
        working_data = {
            "number": 16417,
            "organization": "University of Kentucky",
            "abbreviation": "UKY",
        }
        Naan.objects.create(
            number=working_data["number"],
            organization=working_data["organization"],
            abbreviation=working_data["abbreviation"],
        )
        self.url = reverse("view-naan", kwargs={"number": 16417})
        patch_data = {
            "organization": "Kentucky State University",
        }
        self.client.patch(self.url, patch_data, format="json")
        self.response = self.client.get(self.url, format="json")
        data = self.response.data["data"]
        working_data = {**working_data, **patch_data}
        for key in working_data:
            assert data[key] == working_data[key]
        patch_data = {
            "abbreviation": "KSU",
        }
        self.response = self.client.patch(self.url, patch_data, format="json")
        self.assertEqual(self.response.data["links"]["self"], self.url)
        self.response = self.client.get(self.url, format="json")
        data = self.response.data["data"]
        working_data = {**working_data, **patch_data}
        for key in working_data:
            assert data[key] == working_data[key]

    @pytest.mark.skip("DRF rejects this kind of error in PUT/PATCH requests")
    def test_cannot_update_id(self):
        Naan.objects.create(
            number=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.url = reverse("view-naan", kwargs={"number": 16417})
        data = {
            "number": 16415,
        }
        self.response = self.client.patch(self.url, data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        assert "data" not in self.response.data
        assert "errors" in self.response.data

    def test_delete_naan(self):
        Naan.objects.create(
            number=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.assertEqual(Naan.objects.count(), 1)
        self.url = reverse("view-naan", kwargs={"number": 16417})
        self.response = self.client.delete(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Naan.objects.count(), 0)

    def test_list_naans(self):
        Naan.objects.create(
            number=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        Naan.objects.create(
            number=12026, organization="Library of Congress", abbreviation="USLOC"
        )
        self.url = reverse("naans")
        self.response = self.client.get(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        usloc = {
            "id": 2,
            "number": 12026,
            "organization": "Library of Congress",
            "abbreviation": "USLOC",
        }
        self.assertIn(usloc, self.response.data["data"])


class MinterTests(ApiJwtTestCase):
    def setUp(self):
        self.authenticate()
        Naan.objects.create(
            number=16417,
            organization="University of Kentucky Libraries",
            abbreviation="UKL",
        )

    def test_create_minter(self):
        self.url = reverse("minters", kwargs={"number": 16417})
        data = {
            "shoulder": "tv",
            "template": "tv.sddd",
        }
        self.response = self.client.post(self.url, data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Minter.objects.count(), 1)
        self.assertEqual(Minter.objects.get().naan, Naan.objects.get())
        self.assertEqual(Minter.objects.get().shoulder, "tv")
        self.assertEqual(Minter.objects.get().template, "tv.sddd")

    def test_retrieve_minter(self):
        Minter.objects.create(
            naan=Naan.objects.first(),
            shoulder="tv",
            template="tv.sdd",
        )
        self.url = reverse("view-minter", kwargs={"number": 16417, "shoulder": "tv"})
        self.response = self.client.get(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        data = self.response.data["data"]
        assert data["shoulder"] == "tv"
        assert data["template"] == "tv.sdd"
        assert "state" not in data

    def test_mint_identifiers(self):
        Minter.objects.create(
            naan=Naan.objects.first(),
            shoulder="tv",
            template="tv.sdd",
        )
        self.url = reverse("view-minter", kwargs={"number": 16417, "shoulder": "tv"})
        self.response = self.client.post(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        data = self.response.data["data"]
        assert data["ark"] == "16417/tv00"
        self.response = self.client.post(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        data = self.response.data["data"]
        assert data["ark"] == "16417/tv01"


class RoleTests(ApiJwtTestCase):
    def setUp(self):
        self.authenticate()
        Naan.objects.create(
            number=16417,
            organization="University of Kentucky Libraries",
            abbreviation="UKL",
        )
        Minter.objects.create(
            naan=Naan.objects.first(),
            shoulder="tv",
            template="tv.sdd",
        )

    def test_create_role(self):
        self.url = reverse("roles", kwargs={"number": 16417})
        data = {
            "name": "KUDL",
        }
        self.response = self.client.post(self.url, data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(Role.objects.get().naan, Naan.objects.get())
        self.assertEqual(Role.objects.get().name, "KUDL")


class ArkTests(ApiJwtTestCase):
    def test_create_ark(self):
        self.authenticate()
        Naan.objects.create(
            number=16417,
            organization="University of Kentucky Libraries",
            abbreviation="UKL",
        )
        Minter.objects.create(
            naan=Naan.objects.first(), shoulder="tv", template="tv.sdd"
        )
        minter = Minter.objects.get()
        identifier = minter.mint()
        partial_identifier = identifier.split("/")[1]
        Role.objects.create(name="KUDL")
        self.url = reverse("arks", kwargs={"identifier": identifier})
        self.response = self.client.post(self.url, data={"role_id": 1}, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ark.objects.count(), 1)
        self.assertEqual(Ark.objects.get().role, Role.objects.get())
        self.assertEqual(Ark.objects.get().identifier, identifier)

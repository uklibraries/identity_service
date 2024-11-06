import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from minter.models import Naan
from minter.serializers import NaanSerializer


class RootTests(APITestCase):
    def setUp(self):
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


class NaanTests(APITestCase):
    def tearDown(self):
        self.assertEqual(self.response.data["links"]["self"], self.url)

    def test_create_naan(self):
        self.url = reverse("naans")
        data = {
            "id": 37,
            "organization": "University of Kentucky",
            "abbreviation": "UKY",
        }
        self.response = self.client.post(self.url, data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Naan.objects.count(), 1)
        self.assertEqual(Naan.objects.get().organization, "University of Kentucky")

    def test_retrieve_naan(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.url = reverse("view-naan", kwargs={"naan_id": 16417})
        self.response = self.client.get(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        # Is this just testing the serializer?
        serializer = NaanSerializer(data=self.response.data["data"])
        assert serializer.is_valid()
        self.assertEqual(
            serializer.data,
            {
                "id": 16417,
                "organization": "University of Kentucky",
                "abbreviation": "UKY",
            },
        )

    def test_partial_update_naan(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.url = reverse("view-naan", kwargs={"naan_id": 16417})
        data = {
            "organization": "Kentucky State University",
        }
        self.client.patch(self.url, data, format="json")
        self.response = self.client.get(self.url, format="json")
        serializer = NaanSerializer(data=self.response.data["data"])
        assert serializer.is_valid()
        self.assertEqual(
            serializer.data,
            {
                "id": 16417,
                "organization": "Kentucky State University",
                "abbreviation": "UKY",
            },
        )
        data = {
            "abbreviation": "KSU",
        }
        self.response = self.client.patch(self.url, data, format="json")
        self.assertEqual(self.response.data["links"]["self"], self.url)
        self.response = self.client.get(self.url, format="json")
        serializer = NaanSerializer(data=self.response.data["data"])
        assert serializer.is_valid()
        self.assertEqual(
            serializer.data,
            {
                "id": 16417,
                "organization": "Kentucky State University",
                "abbreviation": "KSU",
            },
        )

    def test_cannot_update_id(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.url = reverse("view-naan", kwargs={"naan_id": 16417})
        data = {
            "nonexistent_id": 16415,
        }
        self.response = self.client.patch(self.url, data, format="json")
        assert "data" not in self.response.data
        assert "errors" in self.response.data

    def test_delete_naan(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.assertEqual(Naan.objects.count(), 1)
        self.url = reverse("view-naan", kwargs={"naan_id": 16417})
        self.response = self.client.delete(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Naan.objects.count(), 0)

    def test_list_naans(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        Naan.objects.create(
            id=12026, organization="Library of Congress", abbreviation="USLOC"
        )
        self.url = reverse("naans")
        self.response = self.client.get(self.url, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        usloc = {
            "id": 12026,
            "organization": "Library of Congress",
            "abbreviation": "USLOC",
        }
        self.assertIn(usloc, self.response.data["data"])

import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from minter.models import Naan
from minter.serializers import NaanSerializer


def test_root_returns_json(api_client):
    url = reverse("root")
    response = api_client.get(url, format="json")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/json"


def test_root_includes_links(api_client):
    url = reverse("root")
    response = api_client.get(url, format="json")
    assert "links" in response.data


def test_root_includes_link_to_naans_resource(api_client):
    url = reverse("root")
    response = api_client.get(url, format="json")
    assert "naans" in response.data["links"]
    assert len(response.data["links"]["naans"]) > 0


class NaanTests(APITestCase):
    def test_create_naan(self):
        url = reverse("naans")
        data = {
            "id": 37,
            "organization": "University of Kentucky",
            "abbreviation": "UKY",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Naan.objects.count(), 1)
        self.assertEqual(Naan.objects.get().organization, "University of Kentucky")

    def test_retrieve_naan(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        url = reverse("view-naan", kwargs={"naan_id": 16417})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Is this just testing the serializer?
        serializer = NaanSerializer(data=response.data)
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
        url = reverse("view-naan", kwargs={"naan_id": 16417})
        data = {
            "organization": "Kentucky State University",
        }
        self.client.patch(url, data, format="json")
        response = self.client.get(url, format="json")
        serializer = NaanSerializer(data=response.data)
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
        self.client.patch(url, data, format="json")
        response = self.client.get(url, format="json")
        serializer = NaanSerializer(data=response.data)
        assert serializer.is_valid()
        self.assertEqual(
            serializer.data,
            {
                "id": 16417,
                "organization": "Kentucky State University",
                "abbreviation": "KSU",
            },
        )

    def test_delete_naan(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        self.assertEqual(Naan.objects.count(), 1)
        url = reverse("view-naan", kwargs={"naan_id": 16417})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Naan.objects.count(), 0)

    def test_list_naans(self):
        Naan.objects.create(
            id=16417, organization="University of Kentucky", abbreviation="UKY"
        )
        Naan.objects.create(
            id=12026, organization="Library of Congress", abbreviation="USLOC"
        )
        url = reverse("naans")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usloc = {
            "id": 12026,
            "organization": "Library of Congress",
            "abbreviation": "USLOC",
        }
        self.assertIn(usloc, response.data)

import pytest

from django.urls import reverse


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

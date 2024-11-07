import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestAuthMixin:
    def authenticate(self):
        user = User.objects.create_user(
            username="test", email="test@example.com", password="testpass"
        )
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url,
            headers={"Content-Type": "application/json"},
            data={"username": "test", "password": "testpass"},
            format="json",
        )
        token = json.loads(response.content.decode())
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")


class ApiJwtTestCase(TestAuthMixin, APITestCase):
    pass

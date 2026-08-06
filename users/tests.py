from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):
    def test_register_user(self):
        data = {"login": "newuser", "email": "new@test.ru", "password": "Test12345!"}
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):
        User.objects.create_user(
            login="testuser", email="test@test.ru", password="test123"
        )
        response = self.client.post(
            "/api/auth/token/", {"login": "testuser", "password": "test123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_profile(self):
        user = User.objects.create_user(
            login="testuser", email="test@test.ru", password="test123"
        )
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/auth/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["login"], "testuser")

    def test_update_profile(self):
        user = User.objects.create_user(
            login="testuser", email="test@test.ru", password="test123"
        )
        self.client.force_authenticate(user=user)
        response = self.client.patch("/api/auth/user/", {"email": "updated@test.ru"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "updated@test.ru")

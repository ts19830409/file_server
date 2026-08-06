from rest_framework import status
from rest_framework.test import APITestCase

from stats.models import UploadStats
from users.models import User


class StatsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            login="testuser", email="test@test.ru", password="test123"
        )
        self.client.force_authenticate(user=self.user)
        UploadStats.objects.create(
            user=self.user, file_name="test.txt", file_size=100, status="success"
        )

    def test_get_stats(self):
        response = self.client.get("/api/stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_stats_only_own(self):
        other_user = User.objects.create_user(
            login="other", email="other@test.ru", password="test123"
        )
        UploadStats.objects.create(
            user=other_user, file_name="other.txt", file_size=200, status="failed"
        )
        response = self.client.get("/api/stats/")
        self.assertEqual(len(response.data), 1)

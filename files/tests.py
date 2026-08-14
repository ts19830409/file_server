from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class FileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            login="testuser", email="test@test.ru", password="test123"
        )
        self.client.force_authenticate(user=self.user)

    def test_upload_file(self):
        file = SimpleUploadedFile(
            "test.txt", b"Hello, World!", content_type="text/plain"
        )
        response = self.client.post(
            "/api/files/",
            {
                "file": file,
                "name_file": "Test File",
                "size_file": 100,
                "content_type": "text/plain",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_file_list(self):
        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_file(self):
        file = SimpleUploadedFile(
            "test.txt", b"Hello, World!", content_type="text/plain"
        )
        upload = self.client.post(
            "/api/files/",
            {
                "file": file,
                "name_file": "Test File",
                "size_file": 100,
                "content_type": "text/plain",
            },
            format="multipart",
        )
        file_id = upload.data["id"]
        response = self.client.delete(f"/api/files/{file_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

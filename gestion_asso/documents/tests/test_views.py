import io
import json
import uuid

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from compta.models import Account
from documents.models import Document


class DocumentUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("test", "test@test.com", "pass")
        self.client.force_authenticate(self.user)

    @override_settings(ALLOWED_UPLOAD_MIMETYPES=["image/jpeg", "image/png"])
    def test_upload_no_image(self):
        resp = self.client.post("/api/documents/upload/", {"category": "achat"})
        self.assertEqual(resp.status_code, 400)

    @override_settings(
        ALLOWED_UPLOAD_MIMETYPES=["image/jpeg", "image/png"],
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        },
    )
    def test_upload_jpeg(self):
        img = io.BytesIO(b"fake-image-data")
        img.name = "test.jpg"
        resp = self.client.post(
            "/api/documents/upload/",
            {"image": img, "category": "achat"},
            format="multipart",
        )
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn("id", data)
        # status stays pending when OCR fails (no Paddle)
        self.assertIn(data["status"], ("pending", "extracted"))

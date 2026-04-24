from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from inventory.models import JewelryCategory, JewelryItem

from .models import Document, DocumentType


User = get_user_model()


@override_settings(MEDIA_ROOT="/tmp/goldledger-test-media")
class DocumentViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="testpass123")
        self.other_user = User.objects.create_user(username="other", password="testpass123")
        self.item = JewelryItem.objects.create(
            user=self.user,
            item_code="GL-100",
            name="Coin",
            category=JewelryCategory.COIN,
            gross_weight=Decimal("4.000"),
        )
        self.other_item = JewelryItem.objects.create(
            user=self.other_user,
            item_code="GL-200",
            name="Private Ring",
            category=JewelryCategory.RING,
            gross_weight=Decimal("7.000"),
        )
        self.document = Document.objects.create(
            item=self.item,
            document_type=DocumentType.BILL,
            title="Invoice",
            file=SimpleUploadedFile("invoice.txt", b"sample bill"),
        )

    def test_document_list_only_shows_owned_item_documents(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(reverse("documents:list", args=[self.item.pk]))
        self.assertContains(response, "Invoice")

    def test_document_upload_blocked_for_other_users_item(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(reverse("documents:create", args=[self.other_item.pk]))
        self.assertEqual(response.status_code, 404)

    def test_document_upload_succeeds_for_owned_item(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.post(
            reverse("documents:create", args=[self.item.pk]),
            {
                "document_type": DocumentType.CERTIFICATE,
                "title": "Purity Certificate",
                "file": SimpleUploadedFile("certificate.txt", b"certificate content"),
            },
        )
        self.assertRedirects(response, reverse("documents:list", args=[self.item.pk]))
        self.assertTrue(Document.objects.filter(item=self.item, title="Purity Certificate").exists())

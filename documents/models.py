from django.db import models

from core.models import UUIDModel
from inventory.models import JewelryItem


class DocumentType(models.TextChoices):
    BILL = "bill", "Bill"
    CERTIFICATE = "certificate", "Certificate"
    PHOTO = "photo", "Photo"
    OTHER = "other", "Other"


class Document(UUIDModel):
    item = models.ForeignKey(JewelryItem, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, default=DocumentType.OTHER)
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="documents/%Y/%m/")
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

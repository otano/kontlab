import uuid

from django.conf import settings
from django.db import models


class Document(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("extracted", "Extrait"),
        ("validated", "Validé"),
        ("rejected", "Rejeté"),
    ]
    FILE_STATUS_CHOICES = [
        ("temp", "Temporaire"),
        ("permanent", "Permanent"),
    ]
    CATEGORY_CHOICES = [
        ("achat", "Achat"),
        ("vente", "Vente"),
        ("cotisation", "Cotisation"),
        ("don", "Don"),
        ("other", "Autre"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    image = models.FileField()
    file_status = models.CharField(
        max_length=10, choices=FILE_STATUS_CHOICES, default="temp"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="achat"
    )

    raw_text = models.TextField(blank=True)

    extracted_date = models.DateField(null=True, blank=True)
    extracted_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    extracted_vat = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    extracted_supplier = models.CharField(max_length=255, blank=True)
    extracted_category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True
    )

    validated_date = models.DateField(null=True, blank=True)
    validated_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    validated_vat = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    validated_supplier = models.CharField(max_length=255, blank=True)
    validated_category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True
    )

    linked_transaction = models.ForeignKey(
        "compta.Transaction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_documents",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "document"
        verbose_name_plural = "documents"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.id} — {self.status}"

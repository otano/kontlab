from django.db import models


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("sent", "Envoyé"),
        ("paid", "Payé"),
        ("cancelled", "Annulé"),
    ]

    number = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField(blank=True)
    date = models.DateField()
    due_date = models.DateField()
    amount_ht = models.DecimalField(max_digits=12, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    amount_ttc = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "facture"
        verbose_name_plural = "factures"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.number} — {self.client_name}"


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="lines"
    )
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "ligne de facture"
        verbose_name_plural = "lignes de facture"

    def __str__(self):
        return f"{self.description} x{self.quantity}"

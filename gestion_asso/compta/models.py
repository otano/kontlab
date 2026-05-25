from django.db import models


class Account(models.Model):
    ACCOUNT_TYPES = [
        ("asset", "Actif"),
        ("liability", "Passif"),
        ("equity", "Fonds propres"),
        ("income", "Produit"),
        ("expense", "Charge"),
        ("treasury", "Trésorerie"),
    ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "compte comptable"
        verbose_name_plural = "plan comptable"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [("expense", "Dépense"), ("revenue", "Recette")]

    date = models.DateField()
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    debit_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="debit_transactions"
    )
    credit_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="credit_transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "écriture comptable"
        verbose_name_plural = "écritures comptables"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.date} — {self.description} ({self.amount} €)"

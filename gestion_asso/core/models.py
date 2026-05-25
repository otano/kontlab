from django.conf import settings
from django.db import models


class Association(models.Model):
    name = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, blank=True)
    address = models.TextField(blank=True)

    default_debit_account = models.CharField(max_length=10, default="606000")
    default_credit_account = models.CharField(max_length=10, default="512000")
    cash_account = models.CharField(max_length=10, default="530000")

    fiscal_year_start = models.DateField(null=True, blank=True)
    fiscal_year_end = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "association"
        verbose_name_plural = "associations"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrateur"),
        ("treasurer", "Trésorier"),
        ("member", "Membre"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    association = models.ForeignKey(
        Association, on_delete=models.SET_NULL, null=True, blank=True, related_name="members"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    class Meta:
        verbose_name = "profil utilisateur"
        verbose_name_plural = "profils utilisateurs"

    def __str__(self):
        return f"{self.user.email} — {self.get_role_display()}"

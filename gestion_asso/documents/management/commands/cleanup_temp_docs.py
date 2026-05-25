from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from documents.models import Document


class Command(BaseCommand):
    help = "Supprime les documents temporaires non validés depuis plus de 2h"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=2)
        expired = Document.objects.filter(
            file_status="temp",
            status__in=["pending", "extracted"],
            uploaded_at__lt=cutoff,
        )
        count = expired.count()
        for doc in expired:
            try:
                if doc.image:
                    storage = doc.image.storage
                    storage.delete(doc.image.name)
            except Exception:
                pass
            doc.delete()
        self.stdout.write(f"{count} document(s) temporaire(s) nettoyé(s)")

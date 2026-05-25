import tempfile

from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from compta.models import Account, Transaction

from .models import Document
from .ocr_engine import parse_receipt
from .s3 import move_to_permanent
from .serializers import (
    DocumentDetailSerializer,
    DocumentListSerializer,
    DocumentUploadSerializer,
    DocumentValidateSerializer,
)


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        image = request.FILES.get("image")
        category = request.data.get("category", "achat")

        if not image:
            return Response({"error": "Image requise"}, status=status.HTTP_400_BAD_REQUEST)

        if image.content_type not in settings.ALLOWED_UPLOAD_MIMETYPES:
            return Response(
                {"error": "Format d'image non supporté (JPEG/PNG uniquement)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        doc = Document.objects.create(
            user=request.user,
            image=image,
            category=category,
            status="pending",
            file_status="temp",
        )

        raw_text = ""
        extracted = {}
        try:
            import paddleocr

            ocr = paddleocr.PaddleOCR(lang="fr", show_log=False)
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                for chunk in image.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            result = ocr.ocr(tmp_path)
            raw_text = "\n".join(
                line[1][0] for line in result[0]
            ) if result and result[0] else ""

            extracted = parse_receipt(raw_text)
            doc.raw_text = raw_text
            doc.extracted_date = extracted.get("date")
            doc.extracted_amount = extracted.get("amount_ttc")
            doc.extracted_vat = extracted.get("vat")
            doc.extracted_supplier = extracted.get("supplier", "")
            doc.extracted_category = category
            doc.status = "extracted"
        except Exception:
            doc.status = "pending"
        finally:
            doc.save(update_fields=[
                "raw_text", "status",
                "extracted_date", "extracted_amount", "extracted_vat",
                "extracted_supplier", "extracted_category",
            ])

        serializer = DocumentUploadSerializer(doc)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocumentValidateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            doc = Document.objects.get(id=pk, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "Document introuvable"}, status=status.HTTP_404_NOT_FOUND)

        if doc.status == "validated":
            return Response({"error": "Déjà validé"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DocumentValidateSerializer(doc, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        doc.validated_date = validated.get("validated_date")
        doc.validated_amount = validated.get("validated_amount")
        doc.validated_vat = validated.get("validated_vat")
        doc.validated_supplier = validated.get("validated_supplier", "")
        doc.validated_category = validated.get("validated_category", doc.category)
        doc.status = "validated"
        doc.file_status = "permanent"

        try:
            if doc.image:
                move_to_permanent(doc.image.name)
        except Exception:
            pass

        category = doc.validated_category or doc.category
        if category == "achat":
            debit_code = "606000"
            credit_code = "512000"
            tx_type = "expense"
        else:
            debit_code = "512000"
            credit_code = "756000" if category == "cotisation" else "758000"
            tx_type = "revenue"

        amount = doc.validated_amount or doc.extracted_amount or 0
        if amount:
            debit_account = Account.objects.filter(code=debit_code).first()
            credit_account = Account.objects.filter(code=credit_code).first()
            if debit_account and credit_account:
                transaction = Transaction.objects.create(
                    date=doc.validated_date or doc.extracted_date or doc.uploaded_at.date(),
                    description=f"Document {doc.id} — {doc.validated_supplier or doc.extracted_supplier}",
                    amount=amount,
                    type=tx_type,
                    debit_account=debit_account,
                    credit_account=credit_account,
                    created_by=request.user,
                )
                doc.linked_transaction = transaction

        doc.save()
        return Response(DocumentDetailSerializer(doc).data)


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentDetailView(generics.RetrieveAPIView):
    serializer_class = DocumentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

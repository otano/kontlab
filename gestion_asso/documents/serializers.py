from rest_framework import serializers

from .models import Document


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id", "status", "raw_text",
            "extracted_date", "extracted_amount", "extracted_vat",
            "extracted_supplier", "extracted_category", "category",
        ]
        read_only_fields = [
            "id", "status", "raw_text",
            "extracted_date", "extracted_amount", "extracted_vat",
            "extracted_supplier", "extracted_category",
        ]


class DocumentValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "validated_date", "validated_amount", "validated_vat",
            "validated_supplier", "validated_category",
        ]

    def validate(self, data):
        instance = self.instance
        if instance and instance.status == "validated":
            raise serializers.ValidationError("Ce document est déjà validé")
        return data


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id", "status", "file_status", "category",
            "uploaded_at", "linked_transaction",
        ]


class DocumentDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"

    def get_image_url(self, obj):
        try:
            return obj.image.url
        except Exception:
            return None

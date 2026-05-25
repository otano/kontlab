from rest_framework import serializers

from .models import Invoice, InvoiceLine


class InvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLine
        fields = "__all__"
        read_only_fields = ["invoice"]


class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "created_by"]


class InvoiceWriteSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "created_by", "number"]

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        invoice = Invoice.objects.create(**validated_data)
        for line_data in lines_data:
            InvoiceLine.objects.create(invoice=invoice, **line_data)
        return invoice

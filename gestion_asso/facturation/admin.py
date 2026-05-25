from django.contrib import admin

from .models import Invoice, InvoiceLine


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["number", "client_name", "date", "amount_ttc", "status"]
    list_filter = ["status", "date"]
    search_fields = ["number", "client_name"]
    inlines = [InvoiceLineInline]

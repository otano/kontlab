from django.contrib import admin

from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "type", "is_active"]
    list_filter = ["type", "is_active"]
    search_fields = ["code", "name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "description", "amount", "type", "debit_account", "credit_account"]
    list_filter = ["type", "date"]

from rest_framework import serializers

from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["created_at", "created_by"]

    def validate(self, data):
        if data["debit_account"] == data["credit_account"]:
            raise serializers.ValidationError(
                "Les comptes débit et crédit doivent être différents"
            )
        return data

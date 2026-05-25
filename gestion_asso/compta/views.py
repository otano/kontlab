from decimal import Decimal

from django.db.models import Sum
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
def balance_view(request):
    accounts = Account.objects.filter(is_active=True)
    data = []
    for account in accounts:
        debit_total = (
            Transaction.objects.filter(debit_account=account).aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )
        credit_total = (
            Transaction.objects.filter(credit_account=account).aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )
        balance = debit_total - credit_total
        data.append(
            {
                "code": account.code,
                "name": account.name,
                "type": account.type,
                "debit_total": str(debit_total),
                "credit_total": str(credit_total),
                "balance": str(balance),
            }
        )
    return Response(data)


@api_view(["GET"])
def result_view(request):
    income = (
        Transaction.objects.filter(type="revenue").aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )
    expense = (
        Transaction.objects.filter(type="expense").aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )
    return Response(
        {
            "total_income": str(income),
            "total_expense": str(expense),
            "net_result": str(income - expense),
        }
    )

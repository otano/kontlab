from django.urls import path

from . import views

urlpatterns = [
    path("accounts/", views.AccountListCreateView.as_view(), name="account-list"),
    path("transactions/", views.TransactionListCreateView.as_view(), name="transaction-list"),
    path("transactions/<int:pk>/", views.TransactionDetailView.as_view(), name="transaction-detail"),
    path("balance/", views.balance_view, name="balance"),
    path("resultat/", views.result_view, name="resultat"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.InvoiceListCreateView.as_view(), name="invoice-list"),
    path("<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice-detail"),
]

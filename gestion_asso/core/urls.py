from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.register_view, name="register"),
    path("me/", views.MeView.as_view(), name="me"),
    path("associations/", views.AssociationListView.as_view(), name="associations"),
]

from django.contrib import admin

from .models import Association, UserProfile


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = ["name", "siret"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "association", "role"]

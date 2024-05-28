from django.contrib import admin

from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    """Configuring admin panel for the User model."""

    list_display = ["email", "is_active", "is_staff", "is_superuser"]
    readonly_fields = ["created_at"]
    fieldsets = [
        (
            "Data",
            {
                "fields": ["email", "is_staff", "is_superuser"],
            },
        ),
        (
            "Meta",
            {
                "classes": ["collapse"],
                "fields": ["created_at", "is_active"],
            },
        ),
    ]

admin.site.register(CustomUser, CustomUserAdmin)

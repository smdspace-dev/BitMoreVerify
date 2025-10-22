from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Show these columns in the admin list view
    list_display = ("id", "username", "email", "is_verified", "is_google_account", "is_staff", "is_superuser", "date_joined")
    list_filter = ("is_verified", "is_google_account", "is_staff", "is_superuser", "is_active")

    # Allow searching by username or email
    search_fields = ("username", "email")

    # Order by newest user first
    ordering = ("-date_joined",)

    # Fields to show in the user detail view
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Verification", {"fields": ("is_verified", "is_google_account")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields to show when adding a new user from admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_verified", "is_google_account", "is_staff", "is_superuser"),
        }),
    )

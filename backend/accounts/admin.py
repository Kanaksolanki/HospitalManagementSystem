from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "get_full_name", "email", "role", "phone", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email", "phone")

    # Add our custom fields onto the stock Django UserAdmin's fieldsets/add form
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Hospital info", {"fields": ("role", "phone")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Hospital info", {"fields": ("role", "phone")}),
    )

    @admin.display(description="Full name")
    def get_full_name(self, obj):
        return obj.get_full_name() or "-"

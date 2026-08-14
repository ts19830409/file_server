from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "login",
        "email",
        "files_count",
        "total_size",
        "created_at",
    ]  # noqa: E501
    search_fields = ["login", "email"]

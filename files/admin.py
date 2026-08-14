from django.contrib import admin

from files.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "name_file",
        "user",
        "size_file",
        "is_public",
        "uploaded_at",
    ]  # noqa: E501
    search_fields = ["name_file", "user__login"]

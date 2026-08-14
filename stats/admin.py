from django.contrib import admin

from stats.models import UploadStats


@admin.register(UploadStats)
class UploadStatsAdmin(admin.ModelAdmin):
    list_display = ["file_name", "user", "status", "uploaded_at"]
    list_filter = ["status"]

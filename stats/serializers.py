from rest_framework import serializers

from stats.models import UploadStats


class UploadStatsSerializer(serializers.ModelSerializer):
    user_login = serializers.ReadOnlyField(source="user.login")

    class Meta:
        model = UploadStats
        fields = [
            "id",
            "user",
            "user_login",
            "file_name",
            "file_size",
            "status",
            "error_message",
            "uploaded_at",
        ]
        read_only_fields = ["user", "uploaded_at"]

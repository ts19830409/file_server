from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "login",
            "email",
            "avatar",
            "created_at",
            "files_count",
            "total_size",
            "success_uploads",
            "failed_uploads",
        ]

        read_only_fields = [
            "created_at",
            "files_count",
            "total_size",
            "success_uploads",
            "failed_uploads",
        ]

from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    user_login = serializers.ReadOnlyField(source="user.login")
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            "id",
            "user",
            "user_login",
            "file",
            "file_url",
            "name_file",
            "size_file",
            "content_type",
            "description",
            "is_public",
            "download_count",
            "share_link",
            "uploaded_at",
        ]
        read_only_fields = [
            "user",
            "download_count",
            "uploaded_at",
            "file_url",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request and obj.file:
            return request.build_absolute_url(obj.file.url)
        return None

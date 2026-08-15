from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    user_login = serializers.ReadOnlyField(source="user.login")
    file_url = serializers.SerializerMethodField()
    format_size = serializers.SerializerMethodField()

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
            "format_size",
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

    def validate(self, data):
        user = self.context["request"].user
        name_file = data.get("name_file")
        size_file = data.get("size_file")

        if File.objects.filter(
            user=user, name_file=name_file, size_file=size_file
        ).exists():
            raise serializers.ValidationError(
                f'Файл "{name_file}" уже существует!'
            )
        return data

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file:
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

    def get_format_size(self, obj):
        return obj.format_size()

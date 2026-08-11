from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "login",
            "email",
            "password",
            "avatar",
            "created_at",
            "files_count",
            "total_size",
            "success_uploads",
            "failed_uploads",
            "first_name",
            "last_name",
        ]

        extra_kwargs = {'password': {'write_only': True}}

        read_only_fields = [
            "created_at",
            "files_count",
            "total_size",
            "success_uploads",
            "failed_uploads",
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

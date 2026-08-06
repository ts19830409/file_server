from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from files.models import File
from files.serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return File.objects.all()
        return File.objects.filter(user=self.request.user)

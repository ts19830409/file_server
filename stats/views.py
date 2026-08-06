from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from stats.models import UploadStats
from stats.serializers import UploadStatsSerializer


class StatsListView(generics.ListAPIView):
    serializer_class = UploadStatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UploadStats.objects.all()
        return UploadStats.objects.filter(user=self.request.user)
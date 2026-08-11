from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from files.models import File
from files.permissions import IsOwner
from files.serializers import FileSerializer
from django.conf import settings
from rest_framework.decorators import action
from django.http import FileResponse
from rest_framework.permissions import AllowAny
from django.db.models import Sum
from rest_framework.exceptions import ValidationError


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'download':
            return File.objects.all()
        if not self.request.user.is_authenticated:
            return File.objects.none()
        if self.request.user.is_staff:
            return File.objects.all()
        return File.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == 'download':
            self.permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create (self, serializer):

        name_file = serializer.validated_data.get('name_file')
        size_file = serializer.validated_data.get('size_file')
    
        existing = File.objects.filter(
            user=self.request.user,
            name_file=name_file,
            size_file=size_file
        ).first()
    
        if existing:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(f'Файл "{name_file}" уже существует!')


        file = serializer.save(user=self.request.user)

        user = self.request.user
        user.files_count = File.objects.filter(user=user).count()
        user.total_size = File.objects.filter(user=user).aggregate(total=Sum('size_file'))['total'] or 0
        user.success_uploads += 1
        user.save()

        share_link = self.request.build_absolute_uri(f'/api/files/{file.id}/download/')
        file.share_link = share_link
        file.save()

        message = f'Файл "{file.name_file}" ({file.size_file} байт) успешно загружен.'
        if file.is_public:
            message += f'\n\nПубличная ссылка для скачивания:\n{share_link}'


        send_mail(
            subject='Файл загружен',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )
        return file

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def download(self, request, pk=None):
        file = self.get_object()
        file.download_count += 1
        file.save()
        return FileResponse(file.file, as_attachment=True)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError:
            user = request.user
            user.failed_uploads += 1
            user.save()
            raise

    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.files_count = File.objects.filter(user=user).count()
        user.total_size = File.objects.filter(user=user).aggregate(total=Sum('size_file'))['total'] or 0
        user.save()
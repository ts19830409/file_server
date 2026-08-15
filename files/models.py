from django.db import models


class File(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Пользователь",
    )
    file = models.FileField(upload_to="uploads/", verbose_name="Файл")
    name_file = models.CharField(max_length=255, verbose_name="Название файла")
    size_file = models.BigIntegerField(default=0, verbose_name="Размер файла в байтах")
    content_type = models.CharField(max_length=100, verbose_name="Тип файла")
    description = models.TextField(blank=True, verbose_name="Описание файла")
    is_public = models.BooleanField(default=False, verbose_name="Публичность")
    download_count = models.IntegerField(
        default=0, verbose_name="Количество скачиваний"
    )
    share_link = models.CharField(
        max_length=255, blank=True, verbose_name="Ссылка для общего доступа"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата загрузки"
    )  # noqa: E501

    def __str__(self):
        return self.name_file

    def format_size(self):
        size = self.size_file
        if size < 1024:
            return f'{size} B'
        elif size < 1024 * 1024:
            return f'{size / 1024:.1f} Kb'
        elif size < 1024 * 1024 * 1024:
            return f'{size / (1024 * 1024):.1f} Mb'
        else:
            return f'{size / (1024 * 1024 * 1024):.1f} Gb'

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ["-uploaded_at"]
        unique_together = ["user", "name_file", "size_file"]


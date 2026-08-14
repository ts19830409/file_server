from django.db import models


class UploadStats(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="upload_stats",
        verbose_name="Пользователь",
    )
    file_name = models.CharField(max_length=255, verbose_name="Имя файла")
    file_size = models.BigIntegerField(verbose_name="Размер файла в байтах")
    status = models.CharField(
        max_length=10,
        choices=[("success", "Успешно"), ("failed", "Ошибка")],
        verbose_name="Статус загрузки",
    )
    error_message = models.TextField(
        blank=True, verbose_name="Сообщение об ошибке"
    )  # noqa: E501
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата загрузки"
    )  # noqa: E501

    def __str__(self):
        return f"{self.file_name} - {self.status}"

    class Meta:
        verbose_name = "Статистика загрузки"
        verbose_name_plural = "Статистика загрузок"
        ordering = ["-uploaded_at"]

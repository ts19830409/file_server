from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not login:
            raise ValueError("Логин обязателен")
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(login, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    login = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    files_count = models.IntegerField(default=0, verbose_name="Общее количество файлов")
    total_size = models.BigIntegerField(default=0, verbose_name="Загружено байтов")
    success_uploads = models.IntegerField(default=0, verbose_name="Успешных загрузок")
    failed_uploads = models.IntegerField(default=0, verbose_name="Неудачных загрузок")

    objects = UserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

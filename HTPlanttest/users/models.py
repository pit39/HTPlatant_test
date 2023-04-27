import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(verbose_name='электронная почта', max_length=128, unique=True)
    full_name = models.CharField(verbose_name='ФИО', max_length=256, blank=True)
    verified = models.BooleanField(verbose_name='верифицированный пользователь', default=False)
    is_staff = models.BooleanField(verbose_name='работник', default=False)
    is_active = models.BooleanField(verbose_name='флаг активности', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email

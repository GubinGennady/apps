from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from config import settings

# Общие настройки для необязательных полей
NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с дополнительными полями.
    Наследуется от AbstractUser для базовой функциональности аутентификации.
    """
    phone_number = models.CharField(max_length=20, **NULLABLE)
    address = models.TextField(**NULLABLE)

    def __str__(self):
        """Строковое представление пользователя (для админки и отладки)"""
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ad(models.Model):
    """
    Модель объявления для системы обмена товарами.
    Содержит информацию о товаре и его состоянии.
    """
    # Варианты состояния товара
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
        ('broken', 'Требует ремонта'),
    ]

    # Категории товаров
    CATEGORY_CHOICES = [
        ('books', 'Книги'),
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(**NULLABLE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default='used')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Отображение в формате: Заголовок (Категория)"""
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']  # Сортировка по убыванию даты создания


class ExchangeProposal(models.Model):
    """
    Модель предложения обмена между двумя объявлениями.
    Отслеживает статус предложения и комментарии.
    """
    # Статусы предложения
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Отображение в формате: Предложение #ID (Статус)"""
        return f"Предложение #{self.id} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        unique_together = ['ad_sender', 'ad_receiver']  # Запрет дублирования предложений
        ordering = ['-created_at']  # Сортировка по дате создания

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from config import settings

NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с дополнительными полями"""
    phone_number = models.CharField(max_length=20, **NULLABLE)
    address = models.TextField(**NULLABLE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ad(models.Model):
    """Модель объявления"""
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
        ('broken', 'Требует ремонта'),
    ]

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
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class ExchangeProposal(models.Model):
    """Модель предложения обмена"""
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
        return f"Предложение #{self.id} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        unique_together = ['ad_sender', 'ad_receiver']
        ordering = ['-created_at']

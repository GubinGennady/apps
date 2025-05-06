from django.contrib import admin
from .models import CustomUser, Ad, ExchangeProposal

# Регистрация модели пользователя в админке
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number') # Отображаемые поля
    search_fields = ('username', 'email')  # Поля для поиска

# Регистрация модели объявлений в админке
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition') # Отображаемые поля
    list_filter = ('category', 'condition')  # Фильтры в правой панели

# Регистрация модели предложений обмена
@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('ad_sender', 'ad_receiver', 'status') # Основная информация
    readonly_fields = ('created_at',)  # Неизменяемые поля
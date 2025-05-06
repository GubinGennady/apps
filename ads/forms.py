from django import forms
from .models import Ad, ExchangeProposal
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

# Форма для создания/редактирования объявлений
class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

        # Кастомизация виджетов для полей формы
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}), # Увеличенное текстовое поле
            'category': forms.Select(choices=Ad.CATEGORY_CHOICES), # Выпадающий список категорий
            'condition': forms.Select(choices=Ad.CONDITION_CHOICES), # Выпадающий список состояний
        }

        # Локализация названий полей
        labels = {
            'image_url': 'Ссылка на изображение',
            'category': 'Категория',
            'condition': 'Состояние'
        }

# Форма для создания предложений обмена
class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']  # Явно указываем нужные поля

        # Настройка виджетов
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}), # Компактное поле для комментария
            'ad_sender': forms.HiddenInput(), # Скрытое поле для отправителя
            'ad_receiver': forms.HiddenInput() # Скрытое поле для получателя
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Принудительная установка обязательных полей
        self.fields['ad_sender'].required = True
        self.fields['ad_receiver'].required = True

# Кастомизированная форма регистрации пользователя
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Поля для регистрации с дополнительными полями
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

# Кастомизированная форма аутентификации
class CustomAuthenticationForm(AuthenticationForm):
    # Локализованные сообщения об ошибках
    error_messages = {
        'invalid_login': "Неверные логин или пароль. Попробуйте снова.",
        'inactive': "Аккаунт неактивен.",
    }
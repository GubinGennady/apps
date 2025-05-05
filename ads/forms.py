from django import forms
from .models import Ad, ExchangeProposal
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(choices=Ad.CATEGORY_CHOICES),
            'condition': forms.Select(choices=Ad.CONDITION_CHOICES),
        }
        labels = {
            'image_url': 'Ссылка на изображение',
            'category': 'Категория',
            'condition': 'Состояние'
        }

# forms.py
class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']  # Явно указываем нужные поля
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'ad_sender': forms.HiddenInput(),
            'ad_receiver': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ad_sender'].required = True
        self.fields['ad_receiver'].required = True
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Неверные логин или пароль. Попробуйте снова.",
        'inactive': "Аккаунт неактивен.",
    }
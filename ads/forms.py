from django import forms
from .models import Ad, ExchangeProposal

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

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'ad_receiver': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'ad_receiver': 'Объявление для обмена',
            'comment': 'Комментарий к предложению'
        }
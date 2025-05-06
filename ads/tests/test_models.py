import pytest
from ads.models import Ad, ExchangeProposal
from django.contrib.auth import get_user_model

User = get_user_model()


# Фикстура для создания тестового пользователя
@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


# Фикстура для создания тестового объявления
@pytest.fixture
def ad(user):
    return Ad.objects.create(
        user=user,
        title='Test Ad',
        description='Test Description',
        category='electronics',
        condition='new'
    )


# Тесты для моделей
@pytest.mark.django_db
def test_ad_creation(ad):
    # Проверка корректности создания объявления
    assert ad.title == 'Test Ad'
    # Проверка строкового представления модели
    assert str(ad) == 'Test Ad (Электроника)'

# tests/test_models.py
import pytest
from ads.models import Ad, ExchangeProposal
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

@pytest.fixture
def ad(user):
    return Ad.objects.create(
        user=user,
        title='Test Ad',
        description='Test Description',
        category='electronics',
        condition='new'
    )

@pytest.mark.django_db
def test_ad_creation(ad):
    assert ad.title == 'Test Ad'
    assert str(ad) == 'Test Ad (Электроника)'
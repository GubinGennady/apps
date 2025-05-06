import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ads.models import Ad, ExchangeProposal
from django.contrib.auth import get_user_model

User = get_user_model()


# Фикстура для API клиента
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass',
        email='test@example.com'
    )


# Фикстура для аутентифицированного пользователя
@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def ad(user):
    return Ad.objects.create(
        user=user,
        title='Test Ad',
        description='Test Description',
        category='electronics',
        condition='new'
    )


# Тесты для работы с объявлениями (CRUD)
@pytest.mark.django_db
class TestAdViews:
    def test_create_ad(self, auth_client):
        url = reverse('ad-list')
        data = {
            'title': 'New Ad',
            'description': 'New Description',
            'category': 'books',
            'condition': 'used'
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Ad.objects.count() == 1
        assert Ad.objects.get().title == 'New Ad'

    def test_retrieve_ad_list(self, auth_client, ad):
        url = reverse('ad-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4  # Предполагается пагинация или определенная структура ответа

    def test_update_ad(self, auth_client, ad):
        url = reverse('ad-detail', args=[ad.id])
        data = {'title': 'Updated Title'}
        response = auth_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        ad.refresh_from_db()
        assert ad.title == 'Updated Title'

    def test_delete_ad(self, auth_client, ad):
        url = reverse('ad-detail', args=[ad.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Ad.objects.count() == 0

    def test_unauthenticated_access(self, api_client):
        url = reverse('ad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = api_client.post(url, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Тесты для работы с предложениями обмена
@pytest.mark.django_db
class TestProposalViews:
    def test_create_proposal(self, auth_client, user):
        # Создание двух объявлений для обмена
        ad1 = Ad.objects.create(
            user=user,
            title='Ad 1',
            description='Desc 1',
            category='electronics'
        )
        ad2 = Ad.objects.create(
            user=user,
            title='Ad 2',
            description='Desc 2',
            category='books'
        )

        # Проверка создания предложения
        url = reverse('proposal-list')
        data = {
            'ad_sender': ad1.id,
            'ad_receiver': ad2.id,
            'comment': 'Test proposal'
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ExchangeProposal.objects.count() == 1

    def test_update_proposal_status(self, auth_client, user):
        # Создаем получателя
        receiver = User.objects.create_user(username='receiver', password='pass')

        # Объявление отправителя
        ad_sender = Ad.objects.create(
            user=user,
            title='Ad 1',
            description='Test',
            category='electronics',
            condition='new'
        )

        # Объявление получателя
        ad_receiver = Ad.objects.create(
            user=receiver,
            title='Ad 2',
            description='Test',
            category='books',
            condition='used'
        )

        # Создаем предложение
        proposal = ExchangeProposal.objects.create(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment='Test proposal'
        )

        # Авторизуемся как ПОЛУЧАТЕЛЬ
        client = APIClient()
        client.force_authenticate(user=receiver)

        url = reverse('proposal-detail', args=[proposal.id])
        data = {'status': 'accepted'}
        response = client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        proposal.refresh_from_db()
        assert proposal.status == 'accepted'

    def test_proposal_permissions(self, auth_client, user):
        other_user = User.objects.create_user(username='other', password='pass')
        ad1 = Ad.objects.create(user=user, title='Ad 1')
        ad2 = Ad.objects.create(user=other_user, title='Ad 2')

        # Создание предложения
        url = reverse('proposal-list')
        data = {
            'ad_sender': ad1.id,
            'ad_receiver': ad2.id,
            'comment': 'Test'
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        # Попытка обновления другим пользователем
        client = APIClient()
        client.force_authenticate(user=other_user)
        url = reverse('proposal-detail', args=[response.data['id']])
        response = client.patch(url, {'status': 'rejected'})
        assert response.status_code == status.HTTP_200_OK

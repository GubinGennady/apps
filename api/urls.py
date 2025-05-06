from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Инициализация маршрутизатора для автоматической генерации URL-путей
router = DefaultRouter()

# Регистрация ViewSet для объявлений (автоматически создаст стандартные CRUD эндпоинты)
router.register(r'ads', views.AdViewSet)

# Регистрация ViewSet для предложений обмена с явным указанием basename
router.register(r'proposals', views.ProposalViewSet, basename='proposal')


urlpatterns = [
    # Включение автоматически сгенерированных URL от роутера
    path('', include(router.urls)),

    # Стандартные эндпоинты для аутентификации DRF (вход/выход через веб-интерфейс)
    path('auth/', include('rest_framework.urls')),

    # Эндпоинты для JWT-аутентификации
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Обновление токена
]

from django.urls import path
from . import views
from .forms import CustomAuthenticationForm

# Пространство имен для организации URL
app_name = 'ads'

urlpatterns = [
    # ============= Основные маршруты =============
    path('', views.HomeView.as_view(), name='home'),  # Домашняя страница
    path('lists/', views.AdListView.as_view(), name='ad-list'),  # Список всех объявлений

    # ============= CRUD для объявлений =============
    path('create/', views.AdCreateView.as_view(), name='ad-create'),  # Создание нового объявления
    path('<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),  # Детали конкретного объявления
    path('<int:pk>/update/', views.AdUpdateView.as_view(), name='ad-update'),  # Редактирование объявления
    path('<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad-delete'),  # Удаление объявления

    # ============= Аутентификация =============
    path('register/', views.RegistrationView.as_view(), name='register'),  # Регистрация пользователя
    path('login/', views.CustomLoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    # Кастомный вход с русской локализацией
    path('logout/', views.logout_user, name='logout'),  # Выход из системы

    # ============= Предложения обмена =============
    # Создание предложения (receiver_id - ID объявления получателя)
    path('propose/<int:receiver_id>/', views.ProposalCreateView.as_view(), name='proposal-create'),
    # Обновление статуса предложения (pk - ID предложения)
    path('proposal/<int:pk>/update/', views.ProposalUpdateView.as_view(), name='proposal-update'),
]

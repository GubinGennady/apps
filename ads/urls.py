from django.urls import path
from . import views
from .forms import CustomAuthenticationForm

app_name = 'ads'

urlpatterns = [
    # Объявления
    path('', views.HomeView.as_view(), name='home'),
    path('lists/', views.AdListView.as_view(), name='ad-list'),
    path('create/', views.AdCreateView.as_view(), name='ad-create'),
    path('<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('<int:pk>/update/', views.AdUpdateView.as_view(), name='ad-update'),
    path('<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad-delete'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Предложения обмена
    path('propose/<int:receiver_id>/', views.ProposalCreateView.as_view(), name='proposal-create'),
    path('proposal/<int:pk>/update/', views.ProposalUpdateView.as_view(), name='proposal-update'),
]
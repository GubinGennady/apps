from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'proposals', views.ProposalViewSet, basename='proposal')  # <-- здесь
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
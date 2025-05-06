from rest_framework import viewsets, permissions
from ads.models import Ad, ExchangeProposal
from api.serializers import AdSerializer, ProposalSerializer
from django.db.models import Q


class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объявлениями через API.
    Обеспечивает полный CRUD функционал.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Автоматически привязывает текущего пользователя к создаваемому объявлению"""
        serializer.save(user=self.request.user)


class ProposalViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления предложениями обмена.
    Ограничивает доступ только к связанным с пользователем предложениям.
    """
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает только предложения, где пользователь является отправителем или получателем"""
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |  # Предложения, отправленные пользователем
            Q(ad_receiver__user=self.request.user)  # Предложения, полученные пользователем
        )

    def get_serializer_context(self):
        """Добавляет объект запроса в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

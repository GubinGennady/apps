from rest_framework import viewsets, permissions
from ads.models import Ad, ExchangeProposal
from api.serializers import AdSerializer, ProposalSerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            ad_sender__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            ad_sender=serializer.validated_data['ad_sender'],
            status='pending'
        )
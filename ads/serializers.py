from rest_framework import serializers
from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('created_at', 'user')
        extra_kwargs = {
            'image_url': {'required': False},
            'description': {'trim_whitespace': False}
        }


class ProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        required=True
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        required=True
    )

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('status', 'created_at')

    def validate(self, data):
        if data['ad_sender'] == data['ad_receiver']:
            raise serializers.ValidationError("Нельзя предлагать обмен на то же объявление")
        return data
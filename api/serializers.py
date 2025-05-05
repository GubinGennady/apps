from rest_framework import serializers
from ads.models import Ad, ExchangeProposal, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']


class AdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['created_at']


class ProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        write_only=True
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        write_only=True
    )

    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment', 'status']
        read_only_fields = ['status']

    def validate(self, data):
        if data['ad_sender'].user != self.context['request'].user:
            raise serializers.ValidationError("Вы не владелец объявления-отправителя")
        return data
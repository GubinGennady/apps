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
        required=False
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        required=False
    )

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, data):
        instance = self.instance

        # При обновлении
        if instance:
            # Проверяем права
            if self.context['request'].user != instance.ad_receiver.user:
                raise serializers.ValidationError(
                    "Только получатель может менять статус"
                )

            # Проверяем допустимость статуса
            if 'status' in data and instance.status != 'pending':
                raise serializers.ValidationError(
                    "Можно менять статус только для ожидающих предложений"
                )

        return data
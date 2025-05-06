from rest_framework import serializers
from ads.models import Ad, ExchangeProposal, CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
   Сериализатор для модели пользователя.
   Отображает основные публичные данные пользователя.
   """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']


class AdSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объявлений с вложенной информацией об авторе.
    Автоматически обрабатывает связанные данные пользователя.
    """
    user = UserSerializer(read_only=True) # Только для чтения, нельзя изменить автора

    class Meta:
        model = Ad
        fields = '__all__'  # Включает все поля модели
        read_only_fields = ['created_at'] # Запрет изменения даты создания


class ProposalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для предложений обмена с расширенной валидацией.
    Обрабатывает логику изменения статуса предложений.
    """
    ad_sender = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        required=False # Может быть установлен автоматически
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        required=False  # Может быть установлен автоматически
    )

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['created_at'] # Дата создания не редактируется

    def validate(self, data):
        """
        Кастомная валидация для проверки:
        1. Прав на изменение статуса
        2. Корректности workflow статусов
        """
        instance = self.instance

        # Логика для операций обновления (PATCH/PUT)
        if instance:
            # Проверяем права
            if self.context['request'].user != instance.ad_receiver.user:
                raise serializers.ValidationError(
                    "Только получатель может менять статус"
                )

            # Проверка что меняем статус только у ожидающих предложений
            if 'status' in data and instance.status != 'pending':
                raise serializers.ValidationError(
                    "Можно менять статус только для ожидающих предложений"
                )

        return data
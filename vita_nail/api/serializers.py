from datetime import datetime
from rest_framework import serializers
from .models import Client, Window, Work
from pytz import UTC


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'surname', 'phone')


class PutClientWindowSerializer(ClientSerializer):
    phone = serializers.CharField(max_length=12)


class WindowSerializer(serializers.ModelSerializer):
    client = PutClientWindowSerializer(required=False)
    is_rewrite = serializers.BooleanField(default=False, allow_null=True)

    class Meta:
        model = Window
        fields = ('date', 'client', 'is_approved', 'is_rewrite')

    def client_forgot_to_rewrite_validator(self, validated_data: dict) -> dict:
        is_rewrite: bool = validated_data.get('is_rewrite')
        client_phone = validated_data.get('client').get('phone')

        client: Client | None = Client.objects.filter(phone=client_phone).first()

        if not client:
            return validated_data

        try:
            clients_latest_datetime: datetime = Window.objects.filter(
                user=client).latest('date').date.replace(tzinfo=UTC)
        except:
            serializers.ValidationError('Клиент уже есть в базе, но нет ни одной записи в окошках')

        datetime_now = datetime.now().replace(tzinfo=UTC)
        if datetime_now < clients_latest_datetime and not is_rewrite:
            raise serializers.ValidationError('У клиента уже есть актуальная запись')

        return validated_data

    def validate(self, attrs: dict) -> dict:
        validated_data = super().validate(attrs)
        if validated_data.get('client'):
            validated_data = self.client_forgot_to_rewrite_validator(validated_data)
        return validated_data

    def create(self, validated_data: dict) -> Window:
        validated_data.pop('is_rewrite')
        return super().create(validated_data)

    def update(self, instance: Window, validated_data: dict) -> Window:
        client_data = validated_data.pop('client')
        self.is_rewrite = validated_data.get('is_rewrite')

        client, created = Client.objects.get_or_create(phone=client_data['phone'], defaults=client_data)
        if self.is_rewrite:
            old_window = Window.objects.filter(client=client).latest()
            old_window.client = None
            old_window.save()
        instance.client = client
        instance.save()
        return instance


class WorkSerializer(serializers.ModelSerializer):
    user = PutClientWindowSerializer()
    window = WindowSerializer()

    class Meta:
        model = Work
        fields = ('user', 'window', 'about', 'price', 'comment', 'date_to_remind')

    def create(self, validated_data: dict):
        user_data = validated_data.pop('user')
        window_data = validated_data.pop('window')
        work = Work.objects.create(**validated_data)
        Client.objects.create(work=work, **user_data)
        Window.objects.create(work=work, **window_data)
        return work

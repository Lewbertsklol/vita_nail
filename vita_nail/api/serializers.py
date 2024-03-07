from datetime import datetime
from typing import Any
from rest_framework import serializers
from .models import User, Window, Work
from pytz import UTC


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'phone')


class PutUserWindowSerializer(UserSerializer):
    phone = serializers.CharField(max_length=12)


class WindowSerializer(serializers.ModelSerializer):
    user = PutUserWindowSerializer(required=False)
    is_rewrite = serializers.BooleanField(default=False, allow_null=True)

    class Meta:
        model = Window
        fields = ('date', 'user', 'is_rewrite')

    def user_unexpected_to_rewrite_validator(self, validated_data: dict) -> dict:
        is_rewrite: bool = validated_data.get('is_rewrite')
        user_phone = validated_data.get('user').get('phone')

        user: User | None = User.objects.filter(phone=user_phone).first()
        if not user:
            return validated_data

        try:
            users_latest_datetime: datetime = Window.objects.filter(
                user=user).latest('date').date.replace(tzinfo=UTC)
        except:
            serializers.ValidationError('Вы есть в базе, но нет записи в окошках')

        datetime_now = datetime.now().replace(tzinfo=UTC)
        if datetime_now < users_latest_datetime and not is_rewrite:
            raise serializers.ValidationError('У Вас уже есть актуальная запись')

        return validated_data

    def validate(self, attrs: dict) -> dict:
        validated_data = super().validate(attrs)
        if validated_data.get('user'):
            validated_data = self.user_unexpected_to_rewrite_validator(validated_data)
        return validated_data

    def create(self, validated_data: dict) -> Window:
        validated_data.pop('is_rewrite')
        return super().create(validated_data)

    def update(self, instance: Window, validated_data: dict) -> Window:
        user_data = validated_data.pop('user')
        is_rewrite = validated_data.get('is_rewrite')
        user, created = User.objects.get_or_create(phone=user_data['phone'], defaults=user_data)
        if is_rewrite:
            old_window = Window.objects.filter(user=user).latest()
            old_window.user = None
            old_window.save()
        instance.user = user
        instance.save()
        return instance


class WorkSerializer(serializers.ModelSerializer):
    user = PutUserWindowSerializer()
    window = WindowSerializer()

    class Meta:
        model = Work
        fields = ('user', 'window', 'about', 'price', 'comment', 'date_to_remind')

    def create(self, validated_data: dict):
        user_data = validated_data.pop('user')
        window_data = validated_data.pop('window')
        work = Work.objects.create(**validated_data)
        User.objects.create(work=work, **user_data)
        Window.objects.create(work=work, **window_data)
        return work

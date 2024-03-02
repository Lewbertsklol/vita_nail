from dataclasses import fields
from rest_framework import serializers
from .models import User, Window, Work


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'phone')


class PutWindowUserSerializer(UserSerializer):
    phone = serializers.CharField(max_length=12)


class WindowSerializer(serializers.ModelSerializer):
    user = PutWindowUserSerializer()

    class Meta:
        model = Window
        fields = ('date', 'user')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user, created = User.objects.get_or_create(phone=user_data['phone'], defaults=user_data)
        instance.user = user
        instance.save()
        return instance


class WorkSerializer(serializers.ModelSerializer):
    user = PutWindowUserSerializer()
    window = WindowSerializer()

    class Meta:
        model = Work
        fields = ('user', 'window', 'about', 'price', 'comment', 'date_to_remind')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        window_data = validated_data.pop('window')
        work = Work.objects.create(**validated_data)
        User.objects.create(work=work, **user_data)
        Window.objects.create(work=work, **window_data)
        return work

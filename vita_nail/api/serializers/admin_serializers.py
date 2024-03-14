from rest_framework import serializers
from ..models import Client, Window, Procedure



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class PutClientWindowSerializer(ClientSerializer):
    phone = serializers.CharField(max_length=12)


class AdminWindowSerializer(serializers.ModelSerializer):
    client = PutClientWindowSerializer(required=False, allow_null=True)
    is_rewrite = serializers.BooleanField(default=False, allow_null=True)

    class Meta:
        model = Window
        fields = '__all__'

    def create(self, validated_data: dict) -> Window:
        del validated_data['is_rewrite']
        return super().create(validated_data)

    def update(self, instance: Window, validated_data: dict) -> Window:
        client_data = validated_data.pop('client')
        self.is_rewrite = validated_data['is_rewrite']
        client, created = Client.objects.get_or_create(phone=client_data['phone'], defaults=client_data)

        if self.is_rewrite:
            old_window = Window.objects.filter(client=client).latest()
            old_window.client = None
            old_window.save()
        instance.client = client
        instance.save()
        return instance


class ProcedureSerializer(serializers.ModelSerializer):
    window = AdminWindowSerializer()

    class Meta:
        model = Procedure
        fields = ('window', 'about', 'price', 'comment', 'date_to_remind')


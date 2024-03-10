import asyncio

from . import serializers
from . import models
from . import bot_notifications

from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.viewsets import ModelViewSet


class AdminClientViewSet(ModelViewSet):
    '''
    Show all clients / create one / delete by admin
    request: /api/v1/admin/clients/
    GET: return all clients
    POST: create new client and return one
    example of body request:
    {
        "name": "example_name",
        "surname": "example_surnamename",
        "phone": "123456789" // unique
    }
    DELETE: delete client by phone
    example of body request:
    {
        "phone": "123456789"
    }
    '''
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]

    def destroy(self, request: Request) -> Response:
        instance = models.Client.objects.filter(phone=request.data['phone']).first()
        if instance:
            instance.delete()
            return Response({
                'client': request.data['phone'],
                'message': 'Client deleted'
            })
        return Response({
            'user': request.data['phone'],
            'message': 'Client not found'
        })


class AdminWindowViewSet(ModelViewSet):
    '''
    Show all windows / create one with client or not / delete by admin
    request: /api/v1/admin/windows/
    GET: return all windows
    POST: create new window and return one
    example of body request:
    {
        "date": "2022-12-12 10-00",
    } 
    or
    {
        "date": "2022-12-12",
        "client": {
            "name": "example_name",
            "surname": "example_surnamename",
            "phone": "123456789" // unique
        }
    } 
    DELETE: delete window by date
    example of body request:
    {
        "date": "2022-12-12 10-00"
    }
    '''
    queryset = models.Window.objects.all()
    serializer_class = serializers.WindowSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]

    def create(self, request: Request) -> Response:
        client_data = request.data.get('client', None)
        if not client_data:
            serializer = serializers.WindowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        if client_data:
            instance, created = models.Window.objects.get_or_create(
                date=request.data['date'],
                defaults={'date': request.data['date']}
            )
            serializer = serializers.WindowSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

    def destroy(self, request: Request) -> Response:
        instance = models.Window.objects.filter(date=request.data['date']).first()
        if instance:
            instance.delete()
            return Response({
                'window': request.data['date'],
                'message': 'Window deleted'
            })
        return Response({
            'window': request.data['date'],
            'message': 'Window not found'
        })


class ClientWindowViewSet(ModelViewSet):
    '''
    Show all free windows or get writing/rewriting to another window by user
    request: /users/windows/
    GET: return all free windows
    PUT: make writing to free findow
    example of body request:
    {
        "date": "2022-12-12 10-00",
    } 
    or 
    {
        "date": "2022-12-12 10-00",
        "user": {
            "name": "example_name",
            "surname": "example_surnamename",
            "phone": "123456789" // unique
        }
    }
    or
    {
        "date": "2022-12-12 10-00",
        "user": {
            "name": "example_name",
            "surname": "example_surnamename",
            "phone": "123456789" // unique
            }
        },
        "is_rewrite": true
    }
    '''
    queryset = models.Window.objects.all()
    serializer_class = serializers.WindowSerializer
    permission_classes = permissions.AllowAny

    def list(self, request):
        windows = models.Window.objects.filter(user=None)
        if len(windows) > 1:
            serializer = serializers.WindowSerializer(windows, many=True)
        serializer = serializers.WindowSerializer(windows)
        return Response(serializer.data)

    def update(self, request):
        instance = models.Window.objects.get(date=request.data['date'])
        serializer = serializers.WindowSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            asyncio.run(bot_notifications.send_notification_by_tgbot(instance))
            return Response(serializer.data)
        return Response(serializer.errors)

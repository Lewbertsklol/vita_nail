import asyncio

from ..serializers import admin_serializers
from .. import models
from .. import bot_notifications

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet


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
    serializer_class = admin_serializers.AdminWindowSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return models.Window.objects.filter(date__year=year, date__month=month)

    def update(self, request):
        instance = models.Window.objects.get(date=request.data['date'])
        serializer = admin_serializers.AdminWindowSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            asyncio.run(bot_notifications.send_notification_by_tgbot(instance))
            return Response(serializer.data)
        return Response(serializer.errors)

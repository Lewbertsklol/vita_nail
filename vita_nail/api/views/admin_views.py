from ..serializers import admin_serializers
from .. import models

from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


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
    serializer_class = admin_serializers.ClientSerializer
    # permission_classes = [permissions.IsAdminUser]
    # authentication_classes = [authentication.TokenAuthentication]

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
    serializer_class = admin_serializers.AdminWindowSerializer
    # permission_classes = [permissions.IsAdminUser]
    # authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return models.Window.objects.filter(date__year=year, date__month=month)

    @action(methods=['post'], detail=False, url_path='(?P<year>.+)/(?P<month>.+)')
    def create(self, request: Request) -> Response:
        client_data = request.data.get('client', None)

        if not client_data:
            serializer = admin_serializers.AdminWindowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        if client_data:
            instance, created = models.Window.objects.get_or_create(
                date=request.data['date'],
                defaults={'date': request.data['date']}
            )
            serializer = admin_serializers.AdminWindowSerializer(instance=instance, data=request.data)
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

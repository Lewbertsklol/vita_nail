from . import serializers
from . import models
from . import bot_notifications
import asyncio
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, authentication_classes



@api_view(['GET', 'POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def admin_users_view(request: Request):
    '''
    Show all users or create one to admin
    request: /admin/users/
    GET: return all users
    POST: create new user and return one
    example of body request:
    {
        "name": "example_name",
        "surname": "example_surnamename",
        "phone": "123456789" // unique
    }
    '''

    if request.method == 'GET':
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def admin_windows_view(request: Request):
    '''
    Show all windows or create one by admin
    request: /admin/windows/
    GET: return all windows
    POST: create new window and return one
    example of body request:
    {
        "date": "2022-12-12 10-00",
    } // create free window
    or
    {
        "date": "2022-12-12",
        "user": {
            "name": "example_name",
            "surname": "example_surnamename",
            "phone": "123456789" // unique
        }
    } // create window for user
    '''

    if request.method == 'GET':
        windows = models.Window.objects.all()
        serializer = serializers.WindowSerializer(windows, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user_data = request.data.get('user', None)
        if not user_data:
            serializer = serializers.WindowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        if user_data:
            instance: models.Window = models.Window.objects.get_or_create(
                date=request.data['date'],
                defaults={'date': request.data['date']}
            )[0]
            serializer = serializers.WindowSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def admin_works_view(request: Request):

    if request.method == 'GET':
        works = models.Work.objects.all()
        serializer = serializers.WorkSerializer(works, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = serializers.WorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def user_windows_view(request: Request):
    '''
    Show all free windows or get writing or rewriting to another window
    request: /users/windows/
    GET: return all free windows
    POST: make writing to free findow
    example of body request:
    {
        "date": "2022-12-12 10-00",
    } // create free window
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

    if request.method == 'GET':
        windows = models.Window.objects.filter(user=None)
        serializer = serializers.WindowSerializer(windows, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        instance = models.Window.objects.get(date=request.data['date'])
        serializer = serializers.WindowSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            asyncio.run(bot_notifications.send_notification_by_tgbot(instance))
            return Response(serializer.data)
        return Response(serializer.errors)

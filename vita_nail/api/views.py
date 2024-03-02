from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET', 'POST'])
def admin_users_view(request: Request):

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


@api_view(['GET', 'POST', 'PUT'])
def admin_windows_view(request: Request):

    if request.method == 'PUT':
        instance = models.Window.objects.get(date=request.data['date'])
        serializer = serializers.WindowSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'GET':
        windows = models.Window.objects.all()
        serializer = serializers.WindowSerializer(windows, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = serializers.WindowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
@api_view(['GET', 'POST', 'PUT'])
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
def user_windows_view(request: Request):
    if request.method == 'PUT':
        instance = models.Window.objects.get(date=request.data['date'])
        serializer = serializers.WindowSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'GET':
        windows = models.Window.objects.filter(user=None)
        serializer = serializers.WindowSerializer(windows, many=True)
        return Response(serializer.data)

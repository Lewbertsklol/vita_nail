from django.urls import path
from . import views


urlpatterns = [
    path('admin/users/', views.AdminClientViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        }
    )),
    path('admin/users/', views.AdminWindowViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'delete': 'destroy'
        }
    )),
]

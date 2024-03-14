from django.urls import path, re_path
from .views import admin_views, client_views


urlpatterns = [
    path('admin/users/', admin_views.AdminClientViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        }
    )),
    path('admin/windows/', admin_views.AdminWindowViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'delete': 'destroy'
        }
    )),
    re_path('windows/(?P<year>.+)/(?P<month>.+)/', client_views.ClientWindowViewSet.as_view(
        {
            'get': 'list',
            'put': 'update'
        }
    ))
]

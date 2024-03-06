from django.urls import path
from . import views


urlpatterns = [
    path('admin/users/', views.admin_users_view),
    path('admin/windows/', views.admin_windows_view),
    path('admin/works/', views.admin_works_view),
    path('windows/', views.user_windows_view),
]

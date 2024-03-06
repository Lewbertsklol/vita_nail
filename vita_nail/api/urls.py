from django.urls import path
from . import views


urlpatterns = [
    path('v1/admin/users/', views.admin_users_view),
    path('v1/admin/windows/', views.admin_windows_view),
    path('v1/admin/works/', views.admin_works_view),
    path('v1/windows/', views.user_windows_view),
]

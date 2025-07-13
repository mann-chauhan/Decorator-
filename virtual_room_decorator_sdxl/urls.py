"""
URL configuration for virtual_room_decorator_sdxl project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('room_decorator.urls')),
] 
from django.urls import path
from . import views
from .views import generate_image

urlpatterns = [
    path('', views.home, name='home'),
]

urlpatterns += [
    path('generate-image/', generate_image, name='generate_image'),
] 
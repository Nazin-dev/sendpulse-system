from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('remove/<int:codigo_cliente>/', views.remove_cliente, name='remove_cliente'),
]

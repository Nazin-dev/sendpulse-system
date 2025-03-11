from django.urls import path
from send import views

urlpatterns = [
    path('', views.home, name='home'),
    path('remove/<int:codigo_cliente>/', views.index_view.remove_cliente, name='remove_cliente'),
    path('campanhas', views.campanhas, name="campanhas")
]

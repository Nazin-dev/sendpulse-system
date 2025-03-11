from django.urls import path
from send import views

urlpatterns = [
    path('', views.home, name='home'),
    path('remove/<int:codigo_cliente>/', views.remove_cliente, name='remove_cliente'),
    path('campanhas', views.campanhas, name="campanhas"),
    path('campanhas/delete/<int:campaign_id>/', views.delete_campaign, name="delete_campaign"),
    path('campanhas/toggle_status/<int:campaign_id>/', views.toggle_campaign_status, name="toggle_campaign_status"),
]

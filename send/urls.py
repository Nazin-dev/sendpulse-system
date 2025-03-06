from django.contrib import admin
from django.urls import path
from send import views

urlpatterns = [
    path('', views.home, name="home"),
]
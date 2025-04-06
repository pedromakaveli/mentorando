from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentorados, name="mentorados"),
    path('reunioes/', views.reunioes, name="reunioes"),
    path('auth/', views.auth, name="auth_mentorado"),
    path('escolher_dia/', views.escolher_dia, name='escolher_dia'),
    path('agendar_reuniao/', views.agendar_reuniao, name='agendar_reuniao')
]
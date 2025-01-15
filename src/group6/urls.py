from django.urls import path
from . import views
app_name = 'group6'
urlpatterns = [
    path('', views.home, name='group6'),
    path('suggest/', views.suggest_word, name='suggest_word'),
    path('system-feedback/', views.system_feedback, name='system_feedback'),
    path('download-text/', views.download_text, name='download_text'),
] 
from django.urls import path
from . import views
app_name = 'group6'
urlpatterns = [
  path('', views.home, name='group6'),
  path('suggest/', views.suggest_word, name='suggest_word'),
  path('rate/', views.rate_word, name='rate_word'),
] 
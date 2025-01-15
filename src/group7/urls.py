from django.urls import path

import registration
from FarsiAid_website.settings import BASE_DIR
from . import views
from .views import *

# from hazm import *

app_name = 'group7'
urlpatterns = [
    path('', views.index, name='home'),
    path('', views.index, name='group7'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),

    path('search/', exact_search_words, name='exact_search_words'),


    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('highlight-words/', highlight_words, name='highlight_words'),
    path('logout/', registration.views.LogoutPage, name='logout'),

    path('add-favorite/', AddFavoriteWordView, name='add_favorite_word'),
    path('remove-favorite/', RemoveFavoriteWordView, name='remove_favorite_word'),
    path('get-favorites/', GetFavoriteWordsView, name='get_favorite_words'),

    path('wordcard/<str:favoriteword>/', views.wordcard, name='wordcard'),

]




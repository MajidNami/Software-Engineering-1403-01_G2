from django.urls import path
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

    # path('about/', views.about, name='about'),
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    #
    # path('searchpage/', views.searchPage, name='searchPage'),
    #
    #
    # path('wordcart/<str:favoriteword>/', views.wordcart, name='wordcart'),

]

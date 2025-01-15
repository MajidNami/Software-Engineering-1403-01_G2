from django.urls import path
from . import views
from . import login_register_view
from django.contrib.auth.decorators import login_required

app_name = 'group1'  
urlpatterns = [
    path('', views.home, name='group1'),
    path('login/', login_register_view.group_login_view, name='group_login'),
    path('signup/', login_register_view.group_register_view, name='group_signup'),
    path('autocomplete/', login_required(views.autocomplete_page), name='autocomplete_page'),
    path('autocomplete/suggestions/', login_required(views.autocomplete_suggestions), name='autocomplete_suggestions'),  # AJAX endpoint for suggestions
     path('update-frequency/', views.update_frequency, name='update_frequency'),
    path('test_frequency/<str:word>/', views.test_word_frequency, name='test_word_frequency'),
]

from django.urls import path
from django.contrib import admin
from . import views

app_name = 'group5'

urlpatterns = [
    path("", views.home, name='group5'),
    path('group5/admin/', admin.site.urls),
    path("text/", views.handle_text_request, name='text'),
    path("file/", views.handle_file_upload, name='file'),
]

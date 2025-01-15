from django.contrib import admin
from .models import G25Dataset


@admin.register(G25Dataset)
class G25DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')
    search_fields = ('word',)

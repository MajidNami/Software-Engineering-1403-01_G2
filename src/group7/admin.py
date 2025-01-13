from django.contrib import admin

from group7.models import *
# Register your models here.

admin.site.register(Word)
admin.site.register(Synonym)
admin.site.register(UserProfile)
admin.site.register(FavoriteWord)
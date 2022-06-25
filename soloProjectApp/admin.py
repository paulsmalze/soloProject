from django.contrib import admin

# Register your models here.
from .models import User,Movie

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','firstName', 'lastName','email',]

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'genre',]   

admin.site.register(User,UserAdmin)
admin.site.register(Movie,MovieAdmin)